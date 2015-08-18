from external.models import *

//CREATE 2 courses, 2 instructors, 1 session and link them

d1 = '2015-02-10'

c1 = Course(name='General Chemistry', code='CHEM1610')
c1.save()
c2 = Course(name='General Chemistry II', code='CHEM1620')
c2.save()

kyle = Instructor(name="Kyle Jones", student_id='kkk321')
kyle.save()
joe = Instructor(name='Joe Speedy', student_id='jmf2rt')
joe.save()

kyle.courses.add(c1)
kyle.courses.add(c2)
kyle.save()

s1 = Session(course=c1, date=d1, instructor=kyle, location='Thornton 005')
s1.save()



