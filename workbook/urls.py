from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^base/$', views.HomeView.as_view(), name='base'),
    url(r'^base/projects$', views.ProjectsView.as_view(), name='projects'),
    url(r'^base/contact$', views.ContactView.as_view(), name='contact'),
    url(r'^base/about$', views.AboutView.as_view(), name='about'),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]