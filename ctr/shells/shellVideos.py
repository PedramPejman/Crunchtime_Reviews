from external.models import *

//CREATE videos and link them to courses



c1 = Course.objects.get(code="CHEM1610")
c2 = Course.objects.get(code="APMA2120")

u1 = User.objects.get(username="kmv5tf")
kyle = Instructor.objects.get(user=u1)

v1 = Video(course=c1, video_url="https://www.youtube.com/watch?v=QS2Kdc4O9Vs", picture_url="http://img.youtube.com/vi/QS2Kdc4O9Vs/hqdefault.jpg", title="Trig Substitution", description="Sometimes, when presented with integrals of the three forms shown in the video, we have the chance to introduce trigonometric functions in order to rewrite the integrand as a derivative of a known inverse trig function (tangent or sine). This is a fairly long process, so we have to have our wits about us!", unit=1, section=2).save()