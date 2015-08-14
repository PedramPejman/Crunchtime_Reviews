from django.forms import ModelForm
from .models import Request

class RequestForm(ModelForm):
	class Meta:
		model = Request
		fields = ['student_id', 'course', 'date', 'description', 'note']
		labels = {
		'student_id': 'Student ID', 
		'course': 'Course',
		'date': 'Date', 
		'description': 'Description',
		'note': 'Additional Notes'
		}

