from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.AccountViewSet, basename='user')

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup")
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
