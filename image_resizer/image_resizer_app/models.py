"""Models."""

from django.db.models import Model
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField


class Image(Model):
	"""Uploaded image model."""

	name = CharField(max_length=255)
	original = ImageField(upload_to='original')
	resized = ImageField(upload_to='resized', null=True)

	def resize(self, width, height):
		print(width, height)
