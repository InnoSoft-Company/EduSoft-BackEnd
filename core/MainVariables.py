from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urlparse

HostURL = "https://www.midoghanam.site"
WebSiteURL = "https://www.midoghanam.site"
#CodeSpaceURL = "https://shiny-computing-machine-rjg65v5p4xxhp9q9-8000.app.github.dev"

def NowURL(request):
  return request.scheme + "://" + request.get_host()

def get_page_url(request):
  referer = request.META.get('HTTP_REFERER', '')
  return urlparse(referer).path if referer else '/'

GoogleOAuth = {
  'client_id': "168962013142-v1t0d4553e4n5evsd2lncbmavhfvqqqg.apps.googleusercontent.com",
  'redirect_uri': f'{HostURL}/auth/oauth/google/callback/',
  'scope': 'openid profile',
  'response_type': 'code',
  'access_type': 'offline',
  'prompt': 'consent',
  "client_secret": "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"
}

#params = {k: v for k, v in GoogleOAuth.items() if k != 'prompt'}

GitHubOAuth = {
  'client_id': 'Ov23li1G33o7ii85wPbM',
  'redirect_uri': f'{HostURL}/auth/oauth/github/callback/',
  'scope': 'read:user',
  'allow_signup': 'true',
  'client_secret': "afdbacf38638f772ae2de5b01a90e8e1a1e080af",
}

BaseURLs = {
  "GoogleOAuth": {
    "auth": "https://accounts.google.com/o/oauth2/v2/auth",
    "getTokens": "https://oauth2.googleapis.com/token",
    "emailAPI": {
      "send": "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
    },
    "user": {
      "info": "https://www.googleapis.com/oauth2/v3/userinfo",
    },

  },
  "GitHubOAuth": {
    "auth": "https://github.com/login/oauth/authorize",
    "getTokens": "https://github.com/login/oauth/access_token",
    'users': "https://api.github.com/user",
    "emails": "https://api.github.com/user/emails",
  },
}

MainVars = {
  "midoghanam": {
    "email": "zentrixproject@gmail.com",
    "gmail": {
      "refresh_token": "",
    }
  }
}

_midoghanam_access_token = {
  "token": None,
  "expires_at": 0
}
