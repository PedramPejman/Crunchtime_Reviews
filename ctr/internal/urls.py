from django.conf.urls import include, url, patterns
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	url(r'^home/$', views.dashboard),
	url(r'^inbox/$', views.inbox),
	url(r'^sessions/$', views.sessions),
	url(r'^sessions/schedule/$', views.sessions_schedule),
	url(r'^sessions/schedule/readme$', TemplateView.as_view(template_name="internal/schedule_readme.html")),
	url(r'^videos/$', views.videos),
	url(r'^videos/readme$', TemplateView.as_view(template_name="internal/video_readme.html")),
	url(r'^settings/$', views.settings),
	url(r'^logout/$', views.logout),

]

