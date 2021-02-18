"""Forms."""

from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import ImageField, IntegerField, URLField


class UploadImage(Form):
	"""Form for uploading image."""

	url_upload = URLField(required=False)
	file_upload = ImageField(required=False)

	def clean(self):
		if bool(self.data.get('url_upload')) == bool(self.files.get('file_upload')):
			raise ValidationError("Выберите что-то одно.")
		return super().clean()


class ResizeImage(Form):
	"""Form for resizing image."""

	width = IntegerField(min_value=8, max_value=2048, required=False)
	height = IntegerField(min_value=8, max_value=2048, required=False)

	def clean(self):
		if not any((self.data.get('width'), self.data.get('height'))):
			raise ValidationError("Введите хотя бы один параметр.")
		return super().clean()
