from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from datetime import datetime, timedelta
from django.views.generic import ListView
from .forms import *
from external.models import *
import calendar

def sessions_show(request):
	#recent_sessions = Session.objects.filter(date__gte= (datetime.now() - timedelta(days=7)))[:5]
	sessions = Session.objects.all()
	today = datetime.today()
	cal = calendar.Calendar()
	month_name = calendar.month_name[today.month]
	days = cal.itermonthdates(today.year, today.month)
	result = []
	for day in days:
		if day.month == today.month: 
			css_class = ''
		else:
			css_class = 'prev-month'
		if len(sessions.filter(date__exact=day)) > 0:
			css_class += 'session-day'
		result.append({'day': day.day, 'class': css_class})
	return render_to_response('sessions/show.html',{'sessions':sessions, 'days': result, 
		'month_name':month_name})

def calendar_show(request):
	sessions = Session.objects.all()
	today = datetime.today()
	cal = calendar.Calendar()
	month_name = calendar.month_name[today.month]
	days = cal.itermonthdates(today.year, today.month)
	result = []
	for day in days:
		if day.month == today.month: 
			css_class = ''
		else:
			css_class = 'prev-month'
		if len(sessions.filter(date__exact=day)) > 0:
			css_class += 'session'
		result.append({'day': day.day, 'class': css_class})

	return render_to_response('sessions/show.html',{'sessions':sessions, 'days': result, 
		'month_name':month_name})	

def sessions_request(request):
	accepted = False
	errors = None
	courses = Course.objects.all()
	print(courses)
	if request.method == 'POST':
		request_form = RequestForm(request.POST)
		if request_form.is_valid():
			accepted = True
			request_form.save()
		else:
			if (request_form.errors):
				errors = request_form.errors
				print(errors)
			else:
				return HttpResponse("Somebody broke this...")
	else:
		request_form = RequestForm()
	return render(request, 'sessions/request.html', {'form':request_form, 'accepted': accepted, 
		'errors': errors, 'courses': courses})


def gallery_show(request):
	BOX_HEIGHT = 162
	BOX_OFFSET = 50
	courses = Course.objects.all()
	refined_courses = []
	for course in courses:
		if len(course.video_set.all()) > 0:
			refined_courses.append(course)
	print(courses)
	div_height = BOX_HEIGHT * len(refined_courses) + BOX_OFFSET
	return render_to_response('gallery/show_courses.html',{'courses':refined_courses, 'div_height':div_height})

def gallery_show_units(request, course_code):
	course = Course.objects.filter(code=course_code)
	raw_videos = Video.objects.filter(course=course)
	if not raw_videos:
		return Http404("Video not found")

	videos = {}
	for video in raw_videos:
		if not video.unit in videos: videos[video.unit] = [video]
		else: videos[video.unit].append(video)
	return render_to_response('gallery/show_units.html', {'videos': videos, 'course': course[0]})

def gallery_show_videos(request, course_code, unit, title, id):
	unit = unit.replace("-", " ").capitalize()
	print(unit, title, id)
	course = Course.objects.filter(code=course_code)
	videos = Video.objects.filter(course=course).filter(unit__iexact=unit)
	if not videos:
		return Http404("Video not found")
	
	return render_to_response('gallery/show_videos.html', {'videos': videos, 'unit': unit, 
		'title': title, 'id': id})

def ask(request):
	return render_to_response('ask/index.html',{})

def about(request):
	return render_to_response('about/index.html',{})