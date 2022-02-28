from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = DefaultRouter()

router.register(r'proof-upload', views.FileUploadViewSet, basename="Proof-Upload")

urlpatterns = []
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls

urlpatterns = router.urls
