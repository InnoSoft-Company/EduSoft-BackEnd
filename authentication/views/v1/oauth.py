from django.contrib.auth import authenticate, login as auth_login
from core.MainVariables import OAuth, BaseURL, WebSiteURL
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model
import secrets, hashlib, hmac, base64, json
from django.shortcuts import redirect
from django.http import JsonResponse
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse
from ... import models as m
import requests, random
from core import JWT

User = get_user_model()

@require_GET
def oauth_redirect(request, oauth_provider=None):
  if not request.method.upper() == "GET": return JsonResponse({"status": False, "error": f"Request method: '{request.method.upper()}' not accepted."}, status=405)
  if not oauth_provider or oauth_provider.lower() not in ["github", "google"]: return redirect(reverse("web-auth-login"))
  action, redirect_to = request.GET.get("action", "").lower(), request.GET.get("redirect", "/").lower()
  state = secrets.token_urlsafe(16)
  raw = json.dumps({"action": action, "state": state, "redirect_to": redirect_to}, separators=(",", ":")).encode()
  token = base64.urlsafe_b64encode(raw + b"." + hmac.new(settings.SECRET_KEY.encode(), raw, hashlib.sha256).digest()).decode()
  request.session['oauth_state'], request.session['oauth_action'] = state, action
  OAuth2 = OAuth["Google" if oauth_provider == "google" else "GitHub"]
  params = {
    "client_id": OAuth2["ClientID"],
    "redirect_uri": BaseURL + reverse("web-auth-oauth-callback", kwargs={"oauth_provider": oauth_provider}), 
    "response_type": "code",
    "scope": OAuth2["scops"][str(action)],
    "state": token
  }
  if oauth_provider == "google": params.update({"access_type": "offline", "prompt": "consent"})
  return redirect(f"{OAuth2['urls']['auth']}?{urlencode(params)}")

@require_GET
def oauth_callback(request, oauth_provider=None):
  code, token = request.GET.get("code"), request.GET.get("state")
  if not code or not token: return blocked_request(request=request, block_type="security")
  try:
    decoded = base64.urlsafe_b64decode(token.encode())
    raw_bytes, hmac_bytes = decoded.rsplit(b".", 1)
    expected_hmac = hmac.new(settings.SECRET_KEY.encode(), raw_bytes, hashlib.sha256).digest()
    if not hmac.compare_digest(expected_hmac, hmac_bytes): return blocked_request(request=request, block_type="security")
    data = json.loads(raw_bytes.decode())
    action, redirect_to = data.get("action"), data.get("redirect_to", "/")
  except Exception as e: return redirect(WebSiteURL + "/login/")
  oauth_provider = oauth_provider.lower()
  if oauth_provider not in ["github", "google"]: return blocked_request(request=request, block_type="maintenance")
  OAuth2 = OAuth["Google" if oauth_provider == "google" else "GitHub"]
  payload = {
    "client_id": OAuth2["ClientID"],
    "client_secret": OAuth2["ClientSecret"],
    "redirect_uri": BaseURL + reverse("web-auth-oauth-callback", kwargs={"oauth_provider": oauth_provider}),
    "code": code,
  }
  if oauth_provider == "google": payload["grant_type"] = "authorization_code"
  r = requests.post(OAuth2["urls"]["token"], data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"}  if oauth_provider == "google" else {"Accept": "application/json"}).json()
  if oauth_provider == "github":
    r = requests.get(OAuth2["urls"]["userinfo"], headers={"Authorization": f"Bearer {r['access_token']}"}).json()
    dec = {
      "sub": r.get("id"),
      "email": r.get("login") + "@github.com",
      "given_name": r.get("name").split(" ")[0],
      "family_name": r.get("name").split(" ")[0:],
    }
    del r
  else:
    id_token = r.get("id_token")
    if not id_token: return redirect(reverse("index"))
    dec = JWT.decode(token=id_token)
  sub = dec.get("sub")
  email = dec.get("email")  
  username = email.split("@")[0]
  while True:
    if User.objects.filter(username=username).exists(): username + str(random.randint(1000, 9999))
    break
  user, user_created = User.objects.get_or_create(username=username, defaults={"email": email, "first_name": dec.get("given_name"), "last_name": dec.get("family_name")})
  oauth_obj, created = m.OAuth.objects.get_or_create(provider_sub=sub, defaults={"provider_sub": sub, "provider": "google", "user": user})
  auth_login(request, oauth_obj.user)
  return redirect(reverse('web-home'))
