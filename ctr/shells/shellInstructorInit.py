from external.models import *

Course(name="Calculus I", code="APMA1090").save()
Course(name="Calculus II", code="APMA1110").save()
Course(name="Calculus III", code="APMA2120").save()
Course(name="Differential Equations", code="APMA2130").save()
Course(name="General Chemistry I", code="CHEM1610").save()
Course(name="General Physics I", code="PHYS1425").save()
Course(name="Program and Data Representation", code="CS2150").save()
Course(name="Digital Logic Design", code="CS2330").save()


instructors = [('pp5nv', 'Pedram', 'Pejman', 'APMA1110', 'Founder'),
('mgs9y',	'Marina', 'Sanusi', '', 'Operations Director'),
('cnh4ph',	'Cherice', 'Hughes-Oliver', 'APMA1090', 'Instructor'),
('be8se',	'Berk', 'Ekmekci', 'CHEM1610', 'Instructor'),
('cjb2ck',	'Christopher', 'Barger', 'CHEM1610', 'Instructor'),
('mt4ze',	'Mariya', 'Tayyab', 'CHEM1610', 'Instructor'),
('esl4rv',	'Emily', 'Leivy', 'APMA2130', 'Instructor'),
('bsc4nj',	'Bakhtiar', 'Chaudry', 'CHEM1610 PHYS1425', 'Instructor'),
('kmv5tf',	'Kyle', 'von Bredow', 'CS2150 CS2330', 'Instructor'),
('rjl2zw',	'Ryan', 'Leiphart', 'APMA2120', 'Instructor'), 
('bam4xz', 'Bridget', 'Mearns', '', 'Administrator'),
('ll4uu', 'Lisa', 'Lampe', '', 'Administrator')]

for i in instructors:
	username = i[0]
	first = i[1]
	last = i[2]
	role = i[4]
	courses = i[3].split()
	u = User.objects.create_user(username=username, first_name=first, last_name=last, password=username)
	u.save()
	ins = Instructor(user=u, role=role)
	ins.save()
	for cname in courses:
		course = Course.objects.get(code=cname)
		ins.courses.add(course)
	ins.save()
