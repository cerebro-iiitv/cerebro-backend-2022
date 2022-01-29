from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.index, name="index"),
    path('list/', views.AccountListView.as_view(), name='account_api'),
    path('create/', views.AccountCreateView.as_view(), name='account-create'),
    path("signup/", views.SignUpApi.as_view(), name="signup"),
    # path("login/", views.LoginApi.as_view(), name="login"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
