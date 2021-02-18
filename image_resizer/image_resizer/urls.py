"""URL Configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls.conf import include
from image_resizer_app.views import ListImages, UploadImage, ResizeImage

urlpatterns = [
	path('image_resizer/', include([
		path('', ListImages.as_view(), name='image-list'),
		path('image/', UploadImage.as_view(), name='image-create'),
		path('image/<pk>/', ResizeImage.as_view(), name='image-update')
	]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
