"""Views."""

from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import FormView

from image_resizer_app.forms import UploadImage as upload_form
from image_resizer_app.models import Image as image_model


class ListImages(ListView):
	"""List uploaded images."""

	template_name = 'image_list.html'
	queryset = image_model.objects.all()


class UploadImage(FormView):
	"""Image uploading form view."""

	template_name = 'upload.html'
	form_class = upload_form

	def form_valid(self, form):
		if file := form.files['file_upload']:
			image = image_model.objects.create(name=file.name, original=file)
		return HttpResponseRedirect(image.original.url)
