from importlib import import_module
from unittest import skip

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import all_products


class TestViewResponses(TestCase):
	def setUp(self):
		self.c = Client()
		self.factory = RequestFactory()
		Category.objects.create(name="django", slug="django")
		User.objects.create(username="admin")
		self.data1 = Product.objects.create(category_id=1, title="django beginners", created_by_id=1, price="20.00", image="django", slug='django-beginners')


	def test_url_allowed_hosts(self):
		"""
		Test Allowed hosts
		"""
		response = self.c.get('/', HTTP_HOST="nodomain.com")
		self.assertEqual(response.status_code, 400)
		response = self.c.get('/', HTTP_HOST="yourdomain.com")
		self.assertEqual(response.status_code, 200)

	def test_product_detail_url(self):
		"""
		Test Product response status
		"""
		response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
		self.assertEqual(response.status_code, 200)

	def test_category_detail_url(self):
		"""
		Test Category response status
		"""
		response = self.c.get(reverse('store:category_detail', args=['django']))
		self.assertEqual(response.status_code, 200)

	def test_homepage_html(self):
		"""
		Example: code validation, search HTML for text
		"""
		request = HttpRequest()
		engine = import_module(settings.SESSION_ENGINE)
		request.session = engine.SessionStore()
		response = all_products(request)
		html = response.content.decode('utf8')
		self.assertIn('<title>Home</title>', html)
		self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
		self.assertEqual(response.status_code, 200)

