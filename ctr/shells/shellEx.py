from django.core.files import File
from external.models import *

d1 = '2015-09-07'
d2 = '2015-09-20'

t1 = '6:30PM'

c1 = Course(name='General Chemistry', code='CHEM1610')
c1.save()
c2 = Course(name='Multivariable Calculus', code='APMA2120')
c2.save()



u1 = User.objects.create_user(username="kmv5tf", password="password", first_name="Kyle", last_name="Jones")
u2 = User.objects.create_user(username="jdb2f", password="password", first_name="Joe", last_name="Speedy")
u3 = User.objects.create_user(username="pp5nv", password="password", first_name="Pedram", last_name="Pejman")
u4 = User.objects.create_user(username="msn4dd", password="password", first_name="Marina", last_name="Sanusi")

kyle = Instructor(user=u1, role="Instructor")
kyle.save()
kyle.picture.save('default.png', File(open('internal/static/internal/employee_pictures/default.jpg', 'rb')))

joe = Instructor(user=u2, role="Instructor")
joe.save()
joe.picture.save('default.png', File(open('internal/static/internal/employee_pictures/default.jpg', 'rb')))

pedram = Instructor(user=u3, role="Founder")
pedram.save()
pedram.picture.save('default.png', File(open('internal/static/internal/employee_pictures/default.jpg', 'rb')))

marina = Employee(user=u4, role="Operations Director")
marina.save()
marina.picture.save('default.png', File(open('internal/static/internal/employee_pictures/default.jpg', 'rb')))


kyle.courses.add(c1)
kyle.courses.add(c2)
kyle.save()
joe.courses.add(c1)
joe.save()
pedram.courses.add(c1)
pedram.save()


s1 = Session(course=c1, date=d1, time=t1, instructor=kyle, location='Thornton 005')
s1.save()

s2 = Session(course=c2, date=d2, time=t1, instructor=pedram, location='Olsson 009')
s2.save()


st1 = Student(student_id="mlh2fa")
st1.save()
r1 = Rating(student=st1, instructor=pedram, session=s2, value = 4.5)
r1.save()
