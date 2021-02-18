"""URL Configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from image_resizer_app.views import ListImages, UploadImage

urlpatterns = [
	path('', ListImages.as_view()),
	path('upload/', UploadImage.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
