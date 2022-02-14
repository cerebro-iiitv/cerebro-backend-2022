from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()

router.register(r'upload', views.FileUploadViewSet, basename="upload")
router.register(r'eventfile-upload', views.FileUploadViewSet, basename="eventfile-upload")

urlpatterns = router.urls