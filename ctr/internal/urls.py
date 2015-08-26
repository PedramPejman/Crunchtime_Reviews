from django.conf.urls import include, url, patterns
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	url(r'^home/$', views.dashboard),
]

