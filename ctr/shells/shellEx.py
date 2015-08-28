from external.models import *

//CREATE 2 courses, 2 instructors, 1 session and link them

d1 = '2015-08-29'
d2 = '2015-08-30'

t1 = '6:30PM'

c1 = Course(name='General Chemistry', code='CHEM1610')
c1.save()
c2 = Course(name='Multivariable Calculus', code='APMA2120')
c2.save()



u1 = User.objects.create_user(username="kmv5tf", password="password", first_name="Kyle", last_name="Jones")
u2 = User.objects.create_user(username="jdb2f", password="password", first_name="Joe", last_name="Speedy")
u3 = User.objects.create_user(username="pp5nv", password="password", first_name="Pedram", last_name="Pejman")

kyle = Instructor(user=u1, role="Instructor")
kyle.save()
joe = Instructor(user=u2, role="Instructor")
joe.save()
pedram = Employee(user=u3, role="Founder")
pedram.save()

kyle.courses.add(c1)
kyle.courses.add(c2)
kyle.save()
joe.courses.add(c1)
joe.save()

s1 = Session(course=c1, date=d1, time=t1, instructor=kyle, location='Thornton 005')
s1.save()

s2 = Session(course=c2, date=d2, time=t1, instructor=joe, location='Olsson 009')
s2.save()



