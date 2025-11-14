from django.urls import path
from .views import signin_view, signout_view, SignupView, CookieTokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', signin_view, name='signin'),
    path('signout/', signout_view, name='signout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]
