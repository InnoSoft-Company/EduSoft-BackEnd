from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .. import views as v

urlpatterns = [
  path("register/", v.v1.auth.RegisterAPIView.as_view(), name="register"),
  path("login/", v.v1.auth.LoginOTPAPIView.as_view(), name="login"),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path("logout/", v.v1.auth.LogoutAPIView.as_view(), name="logout"),

  ## OAuth2 ##
  path("oauth/<str:provider>/", v.v1.oauth.oauth_redirect, name="oauth_redirect"),
  path("oauth/<str:provider>/callback/", v.v1.oauth.oauth_callback, name="oauth_callback"),
]
