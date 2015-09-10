from external.models import *


#GENERAL
crunchtime_host = "crunchtimesupport@virginia.edu"


#ATTEND MAIL
attend_subject = 'Crunchtime Confirmation'

def attend_message(session_id, student_id):
	session = Session.objects.get(id=session_id)
	student = Student.objects.get(student_id=student_id)
	text = "Thank you for registering to attend the crunchtime review session for %s on %s, %s in %s.\n\nIn the mean time, feel free to check out our videos in the website's gallery section.\n\nWe look forward to seeing you!\n\nSincerely,\nYour Humble Crunchers" % (session.course.code, session.date, session.time, session.location) 
	return text


#SCHEDULE MAIL
schedule_subject = 'New Crunchtime Session'

def schedule_message(session):
	return 'Dear Student,\n\nWe are excited to announce that there our instructors have scheduled a review session for your course.\n\nPlease goto crunchtimereviews.com to sign up for the session.\n\nAlso use our "Ask" feature to ask any questions you would like to see worked out at the session.\n\nSincerely,\nYour Humble Crunchers'
	

def schedule_recepients(students):
	emails = []
	for student in students:
		emails.append(student.student_id + "@virginia.edu")
	return emails


#ASK MAIL
ask_subject = 'Crunchtime Request Confirmation'

def ask_message(question):
	return "Dear Student,\n\nThank you for your question. Our instructors will make sure to answer it in your course's next session.\n\nNo session scheduled for your course? Request one on our website!\n\nSincerely, Your Humble Crunchers"


#ASK_ALERT MAIL
ask_alert_subject = 'Crunchtime Request Submitted'

def ask_alert_recepients(instructors):
	emails = []
	for instructor in instructors:
		emails.append(instructor.user.username + "@virginia.edu")
	return emails

def ask_alert_message(question):
	return "Dear Instructor,\n\nThis is a notice that a question for course %s has been submitted by a student.\n\nPlease goto your dashboard or inbox to review details on the question. If you have not already scheduled a session for this course, please consider scheduling one or contacting one of the other %s instructors" %(question.course.code, question.course.code)
