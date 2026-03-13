
from django.test import TestCase, Client
from django.urls import reverse
from .models import *

class NHMModelTest(TestCase):
	def test_model_str(self):
		# Example: test string representation of a model
		# Replace 'YourModel' with actual model name
		# obj = YourModel.objects.create(field1='value')
		# self.assertEqual(str(obj), 'value')
		pass

class NHMViewTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_item_list_view(self):
		response = self.client.get(reverse('item_list'))
		self.assertEqual(response.status_code, 200)
