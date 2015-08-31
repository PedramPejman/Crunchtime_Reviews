from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .forms import *
from external.models import *

def login(request):
	error = None
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user and user.is_active:
			django_login(request, user)
			return HttpResponseRedirect('/internal/home/')
		elif user and not user.is_active:
			error="Your account has been suspended"
		else:
			error="Incorrect username or password"
	return render(request, 'auth/login.html',{'error': error}) 

def logout(request):
	if request.user:
		django_logout(request)
	return HttpResponseRedirect('/.')

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

	sessions = instructor.session_set.all()
	
	upcoming_sessions = sessions.filter(date__gte=today).values()
	previous_sessions = sessions.filter(date__lt=today).values()

	for session in previous_sessions:
		session['rating_percent'] = session['rating'] * 20

	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20

	requests = Request.objects.filter(course__in=instructor.courses.all())
	questions = Question.objects.filter(course__in=instructor.courses.all())


	return render(request, 'internal/home.html', {'user': user, 'rating': rating, 
		'rating_percent': rating_percent, 'upcoming_sessions': upcoming_sessions, 
		'previous_sessions': previous_sessions, 'requests': requests, 'questions': questions})

@login_required
def inbox(request):
	return render(request, 'internal/inbox.html', {})

@login_required
def sessions(request):
	user = request.user
	if not user: return Http404('Error')
	
	today = datetime.today()

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	
	courses = Course.objects.all()
	sessions = instructor.session_set.all()
	
	upcoming_sessions = sessions.filter(date__gte=today).values()
	previous_sessions = sessions.filter(date__lt=today).values()

	for session in previous_sessions:
		session['rating_percent'] = session['rating'] * 20

	rating = Instructor.objects.get(user=user).rating
	rating_percent = rating * 20

	return render(request, 'internal/sessions.html', {'user': user, 'rating': rating, 
		'rating_percent': rating_percent, 'upcoming_sessions': upcoming_sessions, 
		'previous_sessions': previous_sessions})

@login_required
def sessions_schedule(request):
	user = request.user
	if not user: return Http404('Error')
	
	today = datetime.today()

	instructor = Instructor.objects.get(user=user)
	if not instructor: return Http404('Error')
	
	courses = Course.objects.all()
	sessions = instructor.session_set.all()
	
	upcoming_sessions = sessions.filter(date__gte=today).values()
	previous_sessions = sessions.filter(date__lt=today).values()

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
		else:
			errors = scheduleForm.errors

	else:
		scheduleForm = ScheduleForm()


	return render(request, 'internal/schedule.html', {'user': user, 'rating': rating, 
		'rating_percent': rating_percent, 'upcoming_sessions': upcoming_sessions, 
		'previous_sessions': previous_sessions, 'form': scheduleForm, 'accepted': accepted, 'courses': courses})

@login_required
def videos(request):
	return render(request, 'internal/videos.html', {})

@login_required
def settings(request):
	return render(request, 'internal/settings.html', {})
