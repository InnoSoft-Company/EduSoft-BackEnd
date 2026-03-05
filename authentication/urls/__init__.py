from django.urls import path, include

urlpatterns = [
  path("v1/", include("authentication.urls.v1")),
]
