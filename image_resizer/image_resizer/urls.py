"""URL Configuration."""

from django.conf import settings
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.views.static import serve
from image_resizer_app.views import ListImages, ResizeImage, UploadImage

urlpatterns = [
	path('', RedirectView.as_view(url='image_resizer/')),
	path('image_resizer/', include([
		path('', ListImages.as_view(), name='image-list'),
		path('image/', UploadImage.as_view(), name='image-create'),
		path('image/<pk>/', ResizeImage.as_view(), name='image-update')
	])),
	path('images/<path:path>', serve, {'document_root': settings.MEDIA_ROOT})
]
