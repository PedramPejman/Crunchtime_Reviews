from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from .forms import *
from external.models import *

# Create your views here.
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

@login_required
def dashboard(request):
	if (len(Employee.objects.filter(user=request.user))):
		return employee_dashboard(request)
	if (len(Instructor.objects.filter(user=request.user))):
		return instructor_dashboard(request)
	return HttpResponse("Who are you??")
	
def employee_dashboard(request):
	return render(request, 'internal/home.html')

def instructor_dashboard(request):
	return render(request, 'internal/home.html')