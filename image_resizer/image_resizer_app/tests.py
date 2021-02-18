"""Tests."""

import os
from http import HTTPStatus
from io import BytesIO
from random import randbytes

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from PIL import Image

url_list = reverse('image-list')
url_upload = reverse('image-create')
url_resize = (lambda img_id: reverse('image-update', args=(img_id,)))


class UploadImageTest(TestCase):
	"""Tests for uploading image."""

	def generate_image(self, size):
		image = Image.new('RGB', (size, size))
		image.putdata(list(zip(*(randbytes(size ** 2) for _ in range(3)))))
		image_bytes = BytesIO()
		image.save(image_bytes, format='png')
		image_bytes.seek(0)
		image_bytes.name = 'test.png'
		return image_bytes

	def base_test(self, url, template):
		response = self.client.get(url)
		self.assertEqual(response.status_code, HTTPStatus.OK)
		self.assertTemplateUsed(response, 'base.html')
		self.assertTemplateUsed(response, template)
		return response

	def test_get_list(self):
		response = self.base_test(url_list, 'image_list.html')
		self.assertContains(response, f"<a href=\"{url_upload}\">")

	def test_get_upload(self):
		response = self.base_test(url_upload, 'upload.html')
		self.assertContains(response, f"<a href=\"{url_list}\">")

	def test_post_upload(self):
		image_url = url_resize(1)
		response = self.client.get(image_url)
		self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

		image = self.generate_image(500)
		response = self.client.post(url_upload, {'file_upload': image})
		self.assertEqual(response.status_code, HTTPStatus.FOUND)
		self.base_test(image_url, 'resize.html')

		file_path = settings.MEDIA_ROOT / 'original/test.png'
		self.assertTrue(os.path.isfile(file_path))
		os.remove(file_path)
