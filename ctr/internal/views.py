from django.core.files import File
from django.core.mail import send_mail, send_mass_mail
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .forms import *
from external.mail import *
from ctr.settings import DOC_ROOT 
from external.models import *
import re

#MOVE FORWARD

@login_required
def send_course_email(request, session_id):
	user = request.user
	if not user: return Http404('Error')
	
	error = None
	session = Session.objects.get(id=session_id)
	students = session.course.potential_students.all()
	
	email = {}
	email['subject'] = schedule_subject(session)
	email['body'] = schedule_message(session)
	email['students'] = students	
	email['course'] = session.course.name
	accepted = False
	scheduleForm = ScheduleForm()
	if request.method == "POST":
		accepted = True
		try:
			data = (schedule_subject(session), schedule_message(session), crunchtime_host, schedule_recepients(students))
			send_mass_mail((data,))
		except:
			#Check why it failed
			if (len(session.course.students) > 0):
				error = "IMPORTANT: Please let the website administrator know that a notification email was not sent for this session."
			print("Could not send email")
			
		else:
			errors = scheduleForm.errors


	return render(request, 'internal/send_email.html', {'user': user, 'email': email,
		'error': error, 'students': students, 'form': scheduleForm, 'accepted': accepted, 'courses': courses })

@login_required
def courses(request):
	user = request.user
	if not user: return Http404('Error')

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	user_picture = instructor.picture.url

	courses = Course.objects.all()

	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20
	
	return render(request, 'internal/courses.html', {'user': user, 'instructor': instructor, 'user_picture': user_picture,
		'courses': courses, 'rating': rating, 'rating_percent': rating_percent})

def course(request, course_id):	
	user = request.user
	if not user: return Http404('Error')

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	user_picture = instructor.picture.url
	
	course = Course.objects.get(id=course_id)

	instructors = course.instructor_set.all()
	for inst in instructors:
		inst.full_name = inst.name
	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20
	
	potential_students = list(course.potential_students.all())	
	students = course.students
	added_students = []	
	if request.method == 'POST':
		if (len(request.POST['students']) > 3):
			added_students = re.split(' ', request.POST['students'])
		for stud in added_students:
			st = Student(student_id=stud)
			st.save()	
			course.potential_students.add(st)	
		potential_students += added_students

	return render(request, 'internal/course.html', {'user': user, 'instructor': instructor, 'user_picture': user_picture,
		'courses': courses, 'rating': rating, 'potential_students': potential_students, 'students': students, 
		'instructors': instructors,  'rating_percent': rating_percent})



def login(request):
	error = None
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user and user.is_active:
			django_login(request, user)
			return HttpResponseRedirect(DOC_ROOT + 'internal/home/')
		elif user and not user.is_active:
			error="Your account has been suspended"
		else:
			error="Incorrect username or password"
	return render(request, 'auth/login.html',{'error': error}) 

def logout(request):
	if request.user:
		django_logout(request)
	return HttpResponseRedirect(DOC_ROOT)

@login_required
def dashboard(request):
	if (len(Employee.objects.filter(user=request.user))):
		return employee_dashboard(request)
	if (len(Instructor.objects.filter(user=request.user))):
		return instructor_dashboard(request)
	return HttpResponse("Who are you??")

#HELPER	
def employee_dashboard(request):
	return render(request, 'internal/home.html', {})

#HELPER
def instructor_dashboard(request):
	user = request.user
	if not user: return Http404('Error')
	
	today = datetime.today()

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	user_picture = instructor.picture.url

	sessions = instructor.session_set.all()
	
	upcoming_sessions = prepareSessionForTemplate(sessions.filter(date__gte=today).values())
	previous_sessions = prepareSessionForTemplate(sessions.filter(date__lt=today).values())

	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20

	requests = Request.objects.filter(course__in=instructor.courses.all()).order_by('-date_created')
	questions = Question.objects.filter(course__in=instructor.courses.all()).order_by('-date_created')


	return render(request, 'internal/home.html', {'user': user, 
		'user_picture': user_picture, 'rating': rating, 
		'rating_percent': rating_percent, 'upcoming_sessions': upcoming_sessions, 
		'previous_sessions': previous_sessions, 'requests': requests, 'questions': questions})

@login_required
def session_students(request, session_id):
	user = request.user
	if not user: return Http404('Error')

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	
	session = Session.objects.get(id=session_id)
	students = session.students.all()
	
	return render(request, 'internal/session_students.html', {'user': user, 'students': students})

	

@login_required
def inbox(request):
	user = request.user
	if not user: return Http404('Error')

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	user_picture = instructor.picture.url

	requests = Request.objects.filter(course__in=instructor.courses.all())
	questions = Question.objects.filter(course__in=instructor.courses.all())

	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20
	
	return render(request, 'internal/inbox.html', {'user': user, 'instructor': instructor, 'user_picture': user_picture,
		'requests': requests, 'questions': questions, 'rating': rating, 'rating_percent': rating_percent})

@login_required
def sessions(request):
	user = request.user
	if not user: return Http404('Error')
	
	today = datetime.today()

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	user_picture = instructor.picture.url
	
	courses = Course.objects.all()
	sessions = instructor.session_set.all()
	
	upcoming_sessions = prepareSessionForTemplate(sessions.filter(date__gte=today).values())
	previous_sessions = prepareSessionForTemplate(sessions.filter(date__lt=today).values())

	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20

	return render(request, 'internal/sessions.html', {'user': user, 'rating': rating, 
		'rating_percent': rating_percent, 'user_picture': user_picture, 'upcoming_sessions': upcoming_sessions, 
		'previous_sessions': previous_sessions})

@login_required
def sessions_schedule(request):
	user = request.user
	if not user: return Http404('Error')
	
	today = datetime.today()

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	user_picture = instructor.picture.url

	courses = Course.objects.all()
	sessions = instructor.session_set.all()
	error = None
	
	upcoming_sessions = prepareSessionForTemplate(sessions.filter(date__gte=today).values())
	previous_sessions = prepareSessionForTemplate(sessions.filter(date__lt=today).values())

	for session in previous_sessions:
		session['rating_percent'] = session['rating'] * 20

	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20

	accepted = False
	if request.method == "POST":
		scheduleForm = ScheduleForm(request.POST)
		if scheduleForm.is_valid():
			accepted = True
			session = scheduleForm.save(commit=False)
			session.instructor = instructor
			session.save()

			try:
				data = (schedule_subject, schedule_message(session), crunchtime_host, schedule_recepients(session.course.students))
				#Switching to the potential student mass email model
				#send_mass_mail((data,))
			except:
				#Check why it failed
				if (len(session.course.students) > 0):
					error = "IMPORTANT: Please let the website administrator know that a notification email was not sent for this session."
				print("Could not send email")
			
		else:
			errors = scheduleForm.errors

	else:
		scheduleForm = ScheduleForm()

	return render(request, 'internal/schedule.html', {'user': user, 'rating': rating, 'user_picture': user_picture,
		'rating_percent': rating_percent, 'upcoming_sessions': upcoming_sessions, 'error': error,
		'previous_sessions': previous_sessions, 'form': scheduleForm, 'accepted': accepted, 'courses': courses })

@login_required
def videos(request):
	user = request.user
	if not user: return Http404('Error')

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	user_picture = instructor.picture.url

	courses = Course.objects.all()
	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20

	accepted = False
	initial_values = None
	if request.method == "POST":
		videoForm = VideoForm(request.POST)

		if videoForm.is_valid():
			accepted = True
			videoForm.save()
		else:
			initial_values = dict(request.POST)
			for key in initial_values:
				initial_values[key] = initial_values[key][0]		

	else:
		videoForm = VideoForm()

	return render(request, 'internal/videos.html', {'user': user, 'rating': rating, 
		'initial': initial_values, 'rating_percent': rating_percent, 'user_picture': user_picture,
		'form': videoForm, 'accepted': accepted, 'courses': courses})

@login_required
def settings(request):
	user = request.user
	if not user: return Http404('Error')
	
	today = datetime.today()

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	user_picture = instructor.picture.url

	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20
	accepted = False

	if request.method == "POST":
		form = SettingsForm(request.POST, request.FILES)
		if form.is_valid():
			if (len(request.POST['password']) > 0 and len(request.POST['repeat_password']) > 0):
				user.set_password(request.POST['password'])
				user.save()
				accepted = True
			if ('picture' in request.FILES and request.FILES['picture']):
				instructor = Instructor.objects.get(user__username='rjl2zw')
				instructor.picture = request.FILES['picture']
				instructor.save()
				accepted = True
		else :
			print(form.errors)

	else:
		form = SettingsForm()

	return render(request, 'internal/settings.html', {'user': user, 'rating': rating, 'user_picture': user_picture,
		'rating_percent': rating_percent, 'form':form, 'accepted': accepted})

#HELPER FUNCTIONS

def prepareSessionForTemplate(sessions):
	for session in sessions:
		session['rating'] = Session.objects.get(id=session['id']).rating
		session['rating_percent'] = session['rating'] * 20
		session['course'] = Course.objects.get(id=session['course_id']).code
		session['present'] = Session.objects.get(id=session['id']).present
	return sessions
