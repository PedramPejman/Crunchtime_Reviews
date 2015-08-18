from django.conf.urls import include, url, patterns
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name="home.html")),
	url(r'^sessions/request/$', views.sessions_request),
	url(r'^sessions/$', views.sessions_show),
	url(r'^gallery/$', views.gallery_show),
	url(r'^gallery/(?P<course_code>\w+)/$', views.gallery_show_units),
	url(r'^gallery/(?P<course_code>\w+)/(?P<unit>[a-zA-Z0-9\-]+)/((?P<id>\d+)-(?P<title>[a-zA-Z0-9\-]+)){0,1}/$', views.gallery_show_videos),
	url(r'^ask/$', views.ask),
	url(r'^about/$', views.about),
]

