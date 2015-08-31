from django.forms import ModelForm
from external.models import Session

class ScheduleForm(ModelForm):
	class Meta:
		model = Session
		fields = ['course', 'date', 'time', 'location', 'description']
