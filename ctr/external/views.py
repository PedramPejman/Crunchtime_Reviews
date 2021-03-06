from django.core.mail import send_mail, send_mass_mail
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime, timedelta
from django.views.generic import ListView
from .forms import *
from .mail import *
from external.models import *
import calendar

def sessions_show(request):
	#recent_sessions = Session.objects.filter(date__gte= (datetime.now() - timedelta(days=7)))[:5]
	sessions = Session.objects.filter(date__gte=(datetime.now() - timedelta(days=2)))
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

def sessions_plain(request):
	#recent_sessions = Session.objects.filter(date__gte= (datetime.now() - timedelta(days=7)))[:5]
	sessions = Session.objects.all()
	return render_to_response('sessions/plain.html',{'sessions':sessions})


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
	if request.method == 'POST':
		request_form = RequestForm(request.POST)
		if request_form.is_valid():		
			s_request = request_form.save()	
			send_mail(request_subject, request_message(), crunchtime_host, [s_request.student_id+'@virginia.edu'])
			send_mail(request_alert_subject, request_alert_message(s_request), crunchtime_host, request_alert_recepients(s_request))
			accepted = True
		else:
			if (request_form.errors):
				errors = request_form.errors
			else:
				return HttpResponse("Somebody broke this...")
	else:
		request_form = RequestForm()
	return render(request, 'sessions/request.html', {'form':request_form, 'accepted': accepted, 
		'errors': errors, 'courses': courses})

def session_rating(request, sess_id, student_id):
	try:
		print(sess_id)
		session = Session.objects.get(id=int(sess_id))
		print(session)
	except:
		return HttpResponse("This session does not exist")
	try:
		student = Student.objects.get(student_id=student_id)
	except:
		return HttpResponse("This student does not exist")			

	accepted = False
	prev_rating = Rating.objects.filter(student=student, session=session)
	if len(prev_rating) > 0:
		accepted = True
	if not accepted and request.method == 'POST':
		form = RatingForm(request.POST)
		if form.is_valid():
			rate = form.save(commit=False)
			rate.student = student
			rate.session = session
			rate.instructor = session.instructor
			rate.save()
			accepted = True
	else:
		form = RatingForm()
	return render(request, 'sessions/rating.html', {'form':form, 'accepted': accepted, 'student': student,
		'session': session})

def send_rating(request, sess_id):
	#return HttpResponse("no")
	try:
		session = Session.objects.get(id=int(sess_id))
	except:
		return HttpResponse("This session does not exist")

	data = rating_mail_wrap(session)
	
	try:
		number =0
		number = send_mass_mail(data, fail_silently=False)
		print(data)
	except:
		print("could not send email")
		print(data)
		return HttpResponse("Error")

	return HttpResponse("sent %s successful emails" %(number))


def gallery_show(request):
	BOX_HEIGHT = 162
	BOX_OFFSET = 50
	courses = Course.objects.all()
	refined_courses = []
	for course in courses:
		if len(course.video_set.all()) > 0:
			refined_courses.append(course)
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
	course = Course.objects.filter(code=course_code)
	videos = Video.objects.filter(course=course).filter(unit__iexact=unit)
	if not videos:
		return Http404("Video not found")
	
	return render_to_response('gallery/show_videos.html', {'videos': videos, 'unit': unit, 
		'title': title, 'id': id})

def ask(request):
	accepted = False
	errors = None
	courses = Course.objects.all()
	if request.method == 'POST':
		question_form = QuestionForm(request.POST, request.FILES)
		if question_form.is_valid():
			print(request.FILES)
			accepted = True
			question = question_form.save()

			try:
				send_mail(ask_subject, ask_message(question), crunchtime_host, [question.student_id+'@virginia.edu'])
				send_mail(ask_alert_subject, ask_alert_message(question), crunchtime_host, ask_alert_recepients(question.course.instructor_set.all()))
			except:
				print(ask_alert_subject, ask_alert_message(question), crunchtime_host, ask_alert_recepients(question.course.instructor_set.all()))
				print("email was not sent")

		else:
			if (question_form.errors):
				errors = question_form.errors
			else:
				return HttpResponse("Somebody broke this...")
	else:
		question_form = QuestionForm()
	return render(request, 'ask/ask.html', {'form':question_form, 'accepted': accepted, 
		'errors': errors, 'courses': courses})


def about(request):
	instructors = Instructor.objects.all()
	employees = Employee.objects.all()

	return render_to_response('about/about.html',{'instructors': instructors, 'employees': employees})

def attend(request, student_id, session_id):
	session = Session.objects.filter(id=session_id)[0]
	student = Student.objects.filter(student_id=student_id)

	if not student:
		student = Student(student_id=student_id)
		student.save()
		session.students.add(student)
	else:
		student = student[0]
		session.students.add(student)

	try:
		send_mail(attend_subject, attend_message(session_id, student_id), crunchtime_host, [student_id+'@virginia.edu'])
		response = {'status': 'ok'}
	except:
		response = {'status': 'error', 'error': 'mail was not sent'}
		
	return JsonResponse(response)
