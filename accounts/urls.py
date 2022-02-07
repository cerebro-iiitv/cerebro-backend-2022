from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.AccountViewSet, basename='user')

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('password-reset-confirm/<token>', views.ChangePasswordView.as_view(), name='password-reset-confirm'),
    path('request-reset-password/', views.RequestPasswordResetEmail.as_view(), name='request-reset-password'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
