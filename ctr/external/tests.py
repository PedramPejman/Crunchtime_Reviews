from django.test import TestCase
from .models import Course

class ExternalTests(TestCase):

	def should_only_make_valid_courses(self):
		c1 = Course(name='General Chemistry', code='CHEM1610')
		c1.save()
		c2 = Course(name='General Chemistry')
		c2.save()
		self.assertEqual(c1.name, 'General Chemistry')




