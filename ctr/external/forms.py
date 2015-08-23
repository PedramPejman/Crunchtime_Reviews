from django.forms import ModelForm
from .models import Request, Question

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


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ['student_id', 'course', 'text', 'note', 'attachment']
		labels = {
		'student_id': 'Student ID', 
		'course': 'Course',
		'text': 'Problem Description',
		'note': 'Additional Notes',
		'attachment': 'Attach a picture if you want!'
		}

