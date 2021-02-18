"""Views."""

from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import FormView

from image_resizer_app import forms
from image_resizer_app.models import Image


class ListImages(ListView):
	"""List uploaded images."""

	template_name = 'image_list.html'
	queryset = Image.objects.all()


class UploadImage(FormView):
	"""Image uploading form view."""

	template_name = 'upload.html'
	form_class = forms.UploadImage

	def form_valid(self, form):
		if file := form.files['file_upload']:
			image = Image.objects.create(name=file.name, original=file)
		return redirect('image-update', image.pk)


class ResizeImage(FormView):
	"""Image resizing form view."""

	template_name = 'resize.html'
	form_class = forms.ResizeImage

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		# pylint: disable=attribute-defined-outside-init
		self.image = get_object_or_404(Image, pk=kwargs['pk'])
		if not self.image.assert_existence():
			raise Http404()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['image_name'] = self.image.name
		context['image_url'] = (self.image.resized or self.image.original).url
		return context

	def form_valid(self, form):
		self.image.resize(**form.cleaned_data)
		return redirect(self.request.path)
