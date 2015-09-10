from external.models import *

c1 = Course.objects.all()[0]
c2 = Course.objects.all()[1]

s1 = Session.objects.all()[0]
s1 = Session.objects.all()[1]

i1 = Instructor.objects.all()[0]
i2 = Instructor.objects.all()[2]

students = Student.objects.all()
questions = Question.objects.all()
requests = Request.objects.all()
