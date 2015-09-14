from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from .statics import SESSION_STATUS
from datetime import datetime

def courseName(instance, filename):
	return "%s/%s_%s" % (instance.course.code, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), filename)

class Session(models.Model):
	course = models.ForeignKey('Course')
	date = models.DateField()
	date_created = models.DateField(auto_now_add=True)
	time = models.TimeField()
	instructor = models.ForeignKey('Instructor')
	location = models.CharField(max_length=40, null=True)
	description = models.TextField(default="To prepare for the next examination.")
	status = models.CharField(max_length='5', choices=SESSION_STATUS, default=SESSION_STATUS[0])
	test_file = models.FileField(null=True)
	students = models.ManyToManyField('Student')

	@property
	def present(self):
		return len(Student.objects.filter(session=self))

	@present.setter
	def present(self, value):
		pass

	@property
	def rating(self):
		ratings = Rating.objects.filter(session=self).aggregate(Avg('value'))['value__avg']
		if ratings:
			return round(ratings, 2)
		else:
			return 4.0

	@rating.setter
	def rating(self, value):
		pass

	def __str__(self):
		return "Session taught by %s for %s" % (self.instructor.name, self.course.name)

	class Meta:
		ordering = ['-date']

class Course(models.Model):
	name = models.CharField(max_length=30)
	code = models.CharField(max_length=10)

	@property
	def students (self):
		sessions = Session.objects.filter(course=self)
		students = []
		for session in sessions:
			students = students + list(session.students.all())
		return students

	@students.setter
	def students(self, value):
		pass

	def __str__(self):
		return "Course %s: %s" % (self.code, self.name)

class Instructor(models.Model):
	user = models.OneToOneField(User, default=0)
	date_joined = models.DateField(default=datetime.now)
	courses = models.ManyToManyField('Course')
	role = models.CharField(max_length=30, default="Instructor")
	picture = models.ImageField(upload_to="employee_photos", null=True)

	@property
	def name(self):
		return "%s %s" % (self.user.first_name, self.user.last_name)

	@name.setter
	def name(self, value):
		pass
	
	@property
	def rating(self):
		ratings = Rating.objects.filter(instructor=self).aggregate(Avg('value'))['value__avg']
		if ratings:
			return round(ratings, 2)
		else:
			return 4.0

	@rating.setter
	def rating(self, value):
		pass
	
	def __str__(self):
		return "Instructor %s(%s) teaching %s with rating %s" % (self.user.username, self.name, self.courses.all(), self.rating)

class Employee(models.Model):
	user = models.OneToOneField(User, default=0)
	date_joined = models.DateField(default=datetime.now)
	is_admin = models.BooleanField(default=False)
	role = models.CharField(max_length=30)
	picture = models.ImageField(upload_to="employee_photos", null=True)

	@property
	def name(self):
		return "%s %s" % (self.user.first_name, self.user.last_name)

	@name.setter
	def name(self, value):
		pass

class Video(models.Model):
	course = models.ForeignKey('Course')
	title = models.CharField(max_length=50)
	description = models.TextField(default=None)
	unit = models.CharField(max_length=30, default="Miscellaneous")
	section = models.CharField(max_length=30)
	video_url = models.CharField(max_length=100)
	picture_url = models.CharField(max_length=100)

	def __str__(self):
		return "%s for %s(%s - %s)" % (self.title, self.course, self.unit, self.section)

	class Meta:
		ordering= ['unit', 'section', 'title']

	def save(self, *args, **kwargs):
		if (str(self.unit).isdigit()):
			self.unit = "Unit " + str(self.unit)
		super(Video, self).save(*args, **kwargs)


class Request(models.Model):
	course = models.ForeignKey('Course')
	student_id = models.CharField(max_length=10)
	date = models.DateField()
	date_created = models.DateField(auto_now_add=True)
	question_file = models.FileField(null=True)
	description = models.TextField(default=None)
	note = models.TextField(blank=True)

	def __str__(self):
		return "Request by %s for %s " % (self.student_id, self.course)

class Question(models.Model):
	def courseName(instance, filename):
		return "%s/%s_%s" % (instance.course.code, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), filename)

	course = models.ForeignKey('Course')
	student_id = models.CharField(max_length=10)
	date_created = models.DateField(auto_now_add=True)
	attachment = models.FileField(blank=True, null=True, upload_to=courseName)
	text = models.TextField(default=None)
	note = models.TextField(blank=True, null=True)

	def __str__(self):
		return "Question (%s) for %s" % (self.text, self.course)

class Student(models.Model):
	student_id = models.CharField(max_length=10)
	date_created = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.student_id

class Rating(models.Model):
	student = models.ForeignKey('Student')
	instructor = models.ForeignKey('Instructor')
	session = models.ForeignKey('Session')
	value = models.FloatField()
	text = models.TextField(default=None, null=True, blank=True)
