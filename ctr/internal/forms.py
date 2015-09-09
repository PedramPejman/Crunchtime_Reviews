from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from external.models import Session, Video

class ScheduleForm(ModelForm):
	class Meta:
		model = Session
		fields = ['course', 'date', 'time', 'location', 'description']

class VideoForm(ModelForm):
	class Meta:
		model = Video
		fields = ['course', 'title', 'description', 'unit', 'section', 'video_url', 'picture_url']

class SettingsForm(forms.Form):
	password = forms.CharField(max_length=100, required=False)
	repeat_password = forms.CharField(max_length=100, required=False)
	picture = forms.FileField(required=False)

	def clean(self):
		if ('password' in self.cleaned_data):
			if (self.cleaned_data.get('password') !=
				self.cleaned_data.get('repeat_password')):
				raise ValidationError("Passwords do not match")
			if (len(self.cleaned_data.get('password')) < 4):
				raise ValidationError('Password must be at least 4 characters')
		elif ('picture' not in self.cleaned_data):
			raise ValidationError("No changes were submitted")
		return self.cleaned_data