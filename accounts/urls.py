from django.urls import path
from .views import UserProfileAPIView

urlpatterns = [
    path("user/", UserProfileAPIView.as_view()),
]
