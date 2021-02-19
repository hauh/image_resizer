"""Tests."""

import os
from http import HTTPStatus
from io import BytesIO
from random import randbytes
from shutil import rmtree

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from PIL import Image

list_page = reverse('image-list')
upload_page = reverse('image-create')
image_page = (lambda img_id: reverse('image-update', args=(img_id,)))

valid_image_url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"


class UploadImageTest(TestCase):
	"""Tests for uploading image."""

	@classmethod
	def setUpClass(cls):
		settings.MEDIA_ROOT /= 'tests/'
		return super().setUpClass()

	@classmethod
	def tearDownClass(cls):
		rmtree(settings.MEDIA_ROOT)
		return super().tearDownClass()

	def generate_image(self, size=500):
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
		response = self.base_test(list_page, 'image_list.html')
		self.assertContains(response, f"<a href=\"{upload_page}\">")

	def test_get_upload(self):
		response = self.base_test(upload_page, 'upload.html')
		self.assertContains(response, f"<a href=\"{list_page}\">")

	def test_image_404(self):
		response = self.client.get(image_page(1))
		self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

	def test_file_upload(self):
		image = self.generate_image()
		response = self.client.post(upload_page, {'file_upload': image})
		self.assertEqual(response.status_code, HTTPStatus.FOUND)
		self.base_test(image_page(1), 'resize.html')

		file_path = settings.MEDIA_ROOT / 'original' / image.name
		self.assertTrue(os.path.isfile(file_path))

	def test_url_upload(self):
		response = self.client.post(upload_page, {'url_upload': valid_image_url})
		self.assertEqual(response.status_code, HTTPStatus.FOUND)
		self.base_test(image_page(1), 'resize.html')

		file_path = settings.MEDIA_ROOT / 'original' / valid_image_url.split('/')[-1]
		self.assertTrue(os.path.isfile(file_path))

	def test_error_upload(self):
		for wrong_data in (
			{'url_upload': "not an url"},
			{'url_upload': "https://bad.url"},
			{'file_upload': "not a file"},
			{'url_upload': valid_image_url, 'file_upload': self.generate_image()},
			{},
		):
			response = self.client.post(upload_page, wrong_data)
			self.assertIn('form', response.context)
			self.assertFalse(response.context['form'].is_valid())

	def test_resize(self):
		image = self.generate_image()
		self.client.post(upload_page, {'file_upload': image})
		resizing_page = image_page(1)

		for data in (
			{'width': 100, 'height': 100},
			{'width': 10, 'height': 10},
			{'width': 300},
			{'width': 30},
			{'height': 300},
			{'height': 30},
		):
			response = self.client.post(resizing_page, data)
			self.assertEqual(response.status_code, HTTPStatus.FOUND)
			resized_path = settings.MEDIA_ROOT / 'resized' / image.name
			self.assertTrue(os.path.isfile(resized_path))
			check_image = Image.open(resized_path)
			w, h = data.get('width'), data.get('height')
			self.assertEqual(check_image.size, (w or h, h or w))
			check_image.close()

	def test_error_resize(self):
		image = self.generate_image()
		self.client.post(upload_page, {'file_upload': image})
		resizing_page = image_page(1)

		for invalid_value in ("not a number", 0, 1, -100, 5000):
			for field in ('width', 'height'):
				response = self.client.post(resizing_page, {field: invalid_value})
				self.assertIn('form', response.context)
				self.assertFalse(response.context['form'].is_valid())
