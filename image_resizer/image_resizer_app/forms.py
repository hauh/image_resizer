"""Forms."""

from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import ImageField, URLField

errors = {
	'bad_url': {'invalid': "Невалидная ссылка."},
	'bad_image': {'invalid_image': "Невалидное изображение."},
	'multiple_files': "Выберите что-то одно."
}


class UploadImage(Form):
	"""Form for uploading image."""

	url_upload = URLField(required=False, error_messages=errors['bad_url'])
	file_upload = ImageField(required=False, error_messages=errors['bad_image'])

	def clean(self):
		if bool(self.data.get('url_upload')) == bool(self.files.get('file_upload')):
			raise ValidationError(errors['multiple_files'])
		return super().clean()
