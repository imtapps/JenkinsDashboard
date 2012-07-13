from django.conf.urls.defaults import patterns, url

from dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.Index.as_view()),
    url(r'^status/$', views.Status.as_view()),
    url(r'^stats/$', views.Stats.as_view()),
)
