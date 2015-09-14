from django.forms import ModelForm
from django import forms
from .models import Request, Question, Rating

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

class RatingForm(ModelForm):

	class Meta:
		model = Rating
		fields = ['text', 'value']
		labels = ['Additional Notes?', 'How did we do?']




