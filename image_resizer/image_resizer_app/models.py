"""Models."""

from io import BytesIO

from django.core.files.images import ImageFile
from django.db.models import Model
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from PIL import Image as pillow_image


class Image(Model):
	"""Uploaded image model."""

	name = CharField(max_length=255)
	original = ImageField(upload_to='original')
	resized = ImageField(upload_to='resized', null=True)

	def resize(self, width, height):
		image = pillow_image.open(self.original)
		image.thumbnail((width or height, height or width))
		image_bytes = BytesIO()
		image.save(image_bytes, format='png')
		image.close()
		self.resized.delete(save=False)
		self.resized.save(self.name, ImageFile(image_bytes))

	def delete(self):
		self.original.delete(save=False)
		self.resized.delete(save=False)
		return super().delete()

	def assert_existence(self):
		if self.original.storage.exists(self.original.path):
			return True
		self.delete()
		return False
