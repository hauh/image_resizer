"""Forms."""

from django.forms import Form
from django.forms.fields import FileField, URLField
from django.core.exceptions import ValidationError


class UploadImage(Form):
	"""Form for uploading image."""

	url_upload = URLField(required=False)
	file_upload = FileField(required=False)

	def clean(self):
		if bool(self.data['url_upload']) == bool(self.data['file_upload']):
			raise ValidationError("Выберите что-то одно.")
		return super().clean()
