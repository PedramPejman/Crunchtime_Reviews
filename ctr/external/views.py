from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from datetime import datetime, timedelta
from django.views.generic import ListView
from .forms import *
from external.models import *

def sessions_show(request):
	sessions = Session.objects.filter(date__gte= (datetime.now() - timedelta(days=3)))
	for session in sessions:
		print(session)
	return render_to_response('sessions/show.html',{'sessions':sessions})

def sessions_request(request):
	if request.method == 'POST':
		request_form = RequestForm(request.POST)
		if request_form.is_valid():
			return HttpResponse('Done')
		else:
			return HttpResponse("Not a valid form")
	else:
		request_form = RequestForm()
	return render(request, 'sessions/request.html', {'form':request_form})


def gallery_show(request):
	courses = Course.objects.all()
	return render_to_response('gallery/show_courses.html',{'courses':courses})

def gallery_show_units(request, course_code):
	course = Course.objects.filter(code=course_code)
	raw_videos = Video.objects.filter(course=course)
	if not raw_videos:
		return Http404("Video not found")

	videos = {}
	for video in raw_videos:
		if not video.unit in videos: videos[video.unit] = [video]
		else: videos[video.unit].append(video)
	return render_to_response('gallery/show_units.html', {'videos': videos})

def gallery_show_videos(request, course_code, unit, title, id):
	course = Course.objects.filter(code=course_code)
	videos = Video.objects.filter(course=course).filter(unit=unit)
	if not videos:
		return Http404("Video not found")
	
	return render_to_response('gallery/show_videos.html', {'videos': videos})

def ask(request):
	return render_to_response('ask/index.html',{})

def about(request):
	return render_to_response('about/index.html',{})