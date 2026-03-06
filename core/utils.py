from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from .MainVariables import HostURL, OAuth
from django.shortcuts import redirect
from django.conf import settings
from user_agents import parse
import requests, random
import re, requests
from . import JWT

url = HostURL

def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for: return x_forwarded_for.split(',')[0]
  else: return request.META.get('REMOTE_ADDR')

def get_user_agent(request):
  user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
  if user_agent.is_mobile: device_type = "Mobile"
  elif user_agent.is_pc: device_type = "Computer"
  else: device_type = "Unknown Device" 
  return {'device_type': device_type, 'os': user_agent.os.family, 'browser': user_agent.browser.family,}

def exchange_code_google(code):
  data = {
    "code": code,
    "client_id": "15653912530-ti0c8p8ncq7v4va8pi6gikp12jui5k5g.apps.googleusercontent.com",
    "client_secret": "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",
    "redirect_uri": f"{url}/auth/oauth/google/callback/",
    "grant_type": "authorization_code"
  }
  response = requests.post(OAuth["Google"]["urls"]["token"], data=data)
  s = response.status_code
  response = response.json()
  if s == 200: response["id_token"] = JWT.decode_jwt(response["id_token"])
  return response

def generate_code(length=8): return ''.join(str(random.randint(0, 9)) for _ in range(length))

def getUserTokens(user):
  refresh = RefreshToken.for_user(user)
  return {"refresh": str(refresh), "access": str(refresh.access_token),}

def redirectToNext(request, to='/'):
  if isinstance(to, HttpResponseRedirect): to = to.url
  if not isinstance(to, str): to = '/'
  match = re.search(r'(/.*)', to)
  safe_to = match.group(1) if match else '/'
  return redirect(safe_to)
