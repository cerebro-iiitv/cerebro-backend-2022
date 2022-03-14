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
    path('request-reset-password/', views.RequestPasswordReset.as_view(),
         name="request-reset-password"),
    path('password-reset/', views.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('accountcsv/', views.AccountCsvView.as_view(), name="accountcsv")
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
