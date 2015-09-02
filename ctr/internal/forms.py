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
