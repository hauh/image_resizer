"""Views."""

from django.views.generic.edit import FormView
from django.views.generic import ListView

from image_resizer_app.forms import UploadImage as upload_form


class ListImages(ListView):
	"""List uploaded images."""

	template_name = 'image_list.html'
	queryset = ["Image_1", "Image_2", "Image_3"]


class UploadImage(FormView):
	"""Image uploading form view."""

	template_name = 'upload.html'
	form_class = upload_form
