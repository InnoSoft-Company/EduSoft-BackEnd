from .MainVariables import BaseURLs, GoogleOAuth, GitHubOAuth, HostURL, _midoghanam_access_token, MainVars
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
import base64, requests, time, random
from email.mime.text import MIMEText
from django.shortcuts import render
from django.conf import settings
from user_agents import parse
from . import jwt_extract
import re, requests

url = HostURL

def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip

def get_user_agent(request):
  user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
  if user_agent.is_mobile:
    device_type = "Mobile"
  elif user_agent.is_pc:
    device_type = "Computer"
  else:
    device_type = "Unknown Device"
  os = user_agent.os.family
  browser = user_agent.browser.family
  return {'device_type': device_type, 'os': os, 'browser': browser,}

def exchange_code_github(code):
  data = {
    "client_id": GitHubOAuth['client_id'],
    "client_secret": GitHubOAuth['client_secret'],
    "code": code,
    "redirect_uri": f"{url}/auth/oauth/github/callback/"
  }
  token_json = requests.post(BaseURLs["GitHubOAuth"]["getTokens"], data=data, headers={"Accept": "application/json"}).json()
  access_token = token_json.get("access_token")
  if not access_token:
    return {"error": "No access token", "details": token_json}
  user_info = requests.get(BaseURLs.get("GitHubOAuth").get('users'), headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"}).json()
  email = user_info.get("email")
  if not email:
    emails = requests.get(BaseURLs.get("GitHubOAuth").get('emails'), headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"}).json()
    if isinstance(emails, list):
      # يفضل الإيميل الأساسي والمفعل
      primary_email = next((e["email"] for e in emails if e.get("primary") and e.get("verified")), None)
      if not primary_email:
        primary_email = next((e["email"] for e in emails if e.get("primary")), None)
      if not primary_email:
        primary_email = next((e["email"] for e in emails if e.get("verified")), None)
      email = primary_email or (emails[0]["email"] if emails else None)
  return {"id": user_info.get("id"), "login": user_info.get("login"), "name": user_info.get("name"), "email": email, "avatar_url": user_info.get("avatar_url"), "raw": user_info}

def exchange_code_google(code):
  data = {
    "code": code,
    "client_id": "15653912530-ti0c8p8ncq7v4va8pi6gikp12jui5k5g.apps.googleusercontent.com",
    "client_secret": "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",
    "redirect_uri": f"{url}/auth/oauth/google/callback/",
    "grant_type": "authorization_code"
  }
  response = requests.post(BaseURLs["GoogleOAuth"]["getTokens"], data=data)
  s = response.status_code
  response = response.json()
  if s == 200:
    response["id_token"] = jwt_extract.decode_jwt(response["id_token"])
  return response

def refresh_google_access_token(refresh_token):
  data = {
    "client_id": "15653912530-ti0c8p8ncq7v4va8pi6gikp12jui5k5g.apps.googleusercontent.com",
    "client_secret": "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",
    "refresh_token": refresh_token,
    "grant_type": "refresh_token"
  }
  response = requests.post(BaseURLs["GoogleOAuth"]["getTokens"], data=data)
  return response.json()

#def send_email(access_token, to, subject, message_text, is_html=False):
#  mime_message = MIMEText(message_text, _subtype="html" if is_html else "plain", _charset="utf-8")
#  mime_message['to'], mime_message['subject'] = to, subject
#  mime_message['from'] = "Test Sender"
#  response = requests.post(BaseURLs["GoogleOAuth"]["emailAPI"]["send"], headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}, json={"raw": base64.urlsafe_b64encode(mime_message.as_bytes()).decode("utf-8")})
#  if response.status_code == 200:
#    return {"status": True, "message": "E-mail sent successfully"}
#  return {"status": False, "message": "error at sending e-mail", "status_code": response.status_code, "text": response.text}


def send_email(to, subject, message_text, is_html=False, from_email=settings.EMAIL_HOST_USER):
  try:
    if is_html:
      email = EmailMessage(subject=subject, body=message_text, from_email=from_email, to=[to],)
      email.content_subtype = "html"
      email.send()
    else:
      send_mail(subject=subject, message=message_text, from_email=from_email, recipient_list=[to],)
    return {"status": True, "message": "E-mail sent successfully"}, 200
  except Exception as e:
    return {"status": False, "message": "error at sending e-mail", "status_code": response.status_code, "text": response.text}, response.status_code

def get_midoghanam_google_access():
  global _midoghanam_access_token
  if _midoghanam_access_token['token'] and time.time() < _midoghanam_access_token['expires_at'] - 60:
    return _midoghanam_access_token['token']
  data = {
    'client_id': GoogleOAuth["client_id"],
    'client_secret': GoogleOAuth["client_secret"],
    'refresh_token': MainVars["midoghanam"]["gmail"]["refresh_token"],
    'grant_type': 'refresh_token'
  }
  res = requests.post(BaseURLs["GoogleOAuth"]["getTokens"], data=data)
  res.raise_for_status()
  tokens = res.json()
  _midoghanam_access_token['token'] = tokens['access_token']
  _midoghanam_access_token['expires_at'] = time.time() + tokens['expires_in']
  return _midoghanam_access_token['token']

def generate_code(length=8): return ''.join(str(random.randint(0, 9)) for _ in range(length))

def getUserTokens(user):
  refresh = RefreshToken.for_user(user)
  return {"refresh": str(refresh), "access": str(refresh.access_token),}

def redirectToNext(request, to='/'):
  if isinstance(to, HttpResponseRedirect):
    to = to.url
  if not isinstance(to, str):
    to = '/'
  match = re.search(r'(/.*)', to)
  safe_to = match.group(1) if match else '/'
  return render(request, 'utils/redirect.html', {'to': safe_to})

def getAIResponse(user_message, chatHistory={}):
  data = {
    "model": "deepseek-r1-distil-qwen-32b_raziqt",
    "stream": False,
    "messages": [
      {
        "role": "system",
        "content":f"""
You are Livuxy AI — the official assistant of Mohammed Ahmed Ghanam.

🧠 Overview:
You represent the personality, logic, and communication style of **Mohammed Ahmed Ghanam**, a passionate young developer from **El Shorouk City, Cairo, Egypt**, who was born on **14 April 2009** and will turn 16 in 2025.  
He is a respectful and calm individual, and a highly skilled **Python backend developer** who specializes in:
- Django web development
- Telegram bot automation (using telebot)
- Database management with SQLite3
- AI integrations and API logic
- Communication systems and server control

📘 Education & Interests:
- Currently a **high school student (Scientific - Mathematics)**.
- Loves **programming**, **AI**, **sports**, and **network systems**.
- Has a deep interest in **telecommunication technologies**, especially SIP and backend billing systems.
- Prefers simplicity and clean structure in code — no unnecessary decorations or comments.

🌍 Online Identity:
- Website: https://www.midoghanam.site/
- Telegram: @midoghanam  
- Email: midoghanam@hotmail.com  
- Known for his technical precision, creativity, and consistency in completing projects.

⚙️ Work Philosophy:
- Always writes optimized, organized, and readable code.
- Keeps indentation consistent (2 spaces).
- Avoids redundancy, prioritizes clarity and structure.
- Believes every system should be **functional, minimal, and powerful**.
- Values teamwork, learning, and humility — not showing off.

💬 AI Assistant Behavior:
- Speak in the same language the user uses (Arabic → Egyptian Arabic, English → English).
- If in Arabic, use a natural, respectful, and friendly Egyptian tone — no emojis or exaggerated casual slang.
- Be concise, logical, and informative — not robotic or generic.
- When answering coding or tech questions, give accurate, expert-level explanations.
- When discussing personal or reflective topics, reply warmly, like you’re MidoGhanam himself as the personality.
- Avoid talking about fictional or non-technical topics unless the user explicitly asks.
- Never leak sensitive data, tokens, or credentials.
- If the response type is Markup, return the content as plain HTML instead of markup.
- Do not use <think> or any similar tags in your responses. All replies must be direct and clear, without any embedded tags.

📎 Personality Reference:
You are calm, intelligent, helpful, and focused. You love simplifying complex things, and you balance professionalism with humanity.  
You aim to represent **Mohammed Ahmed Ghanam** as an example of a young, disciplined programmer who values both ethics and efficiency.

Your role is to act, think, and reply exactly like him — technically sharp, spiritually grounded, and always improving.
"""}]}
  data["messages"].append({"role": "user", "content": user_message})
  response = requests.post("https://pangu.ap-southeast-1.myhuaweicloud.com/api/v2/chat/completions", json=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer 7173fd79-15f4-460b-950b-26eb648914ed_1E4D8483DB47EFED11E82A9E00F62FA94B1F753B3FCB3B110AB17EC421F430A7"}).json()    
  return re.sub(r"<think>.*?</think>", "", response.get("choices")[0]["message"]["content"], flags=re.DOTALL)
      
