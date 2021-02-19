"""Forms."""

from io import BytesIO
from urllib import parse, request
from urllib.error import HTTPError, URLError

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.forms import Form
from django.forms.fields import ImageField, IntegerField, URLField


class UploadImage(Form):
	"""Form for uploading image."""

	url_upload = URLField(required=False)
	file_upload = ImageField(required=False)

	def clean(self):
		if bool(self.data.get('url_upload')) == bool(self.files.get('file_upload')):
			raise ValidationError("Выберите что-то одно.")

		cleaned_data = super().clean()

		if url_upload := cleaned_data.get('url_upload'):
			try:
				response = request.urlopen(url_upload)

				content_type = response.getheader('Content-Type')
				if not content_type or not content_type.startswith('image'):
					raise ValidationError("Ссылка не похожа на изображение.")

				content_length = int(response.getheader('Content-Length', 0))
				if content_length > settings.FILE_UPLOAD_MAX_SIZE:
					raise ValidationError("Слишком большой файл.")

				image_bytes = BytesIO()
				while chunk := response.read(1024 * 1024):
					image_bytes.write(chunk)
					if image_bytes.tell() > settings.FILE_UPLOAD_MAX_SIZE:
						raise ValidationError("Слишком большой файл.")

			except (HTTPError, URLError) as e:
				raise ValidationError("Ошибка скачивания файла.") from e

			image_name = parse.urlparse(response.url).path.split('/')[-1]
			if '.' not in image_name:
				image_name += '.' + content_type.removeprefix('image/')
			self.files['url_upload'] = ImageFile(image_bytes, name=image_name)

		return cleaned_data


class ResizeImage(Form):
	"""Form for resizing image."""

	width = IntegerField(min_value=8, max_value=2048, required=False)
	height = IntegerField(min_value=8, max_value=2048, required=False)

	def clean(self):
		if not any((self.data.get('width'), self.data.get('height'))):
			raise ValidationError("Введите хотя бы один параметр.")
		return super().clean()
