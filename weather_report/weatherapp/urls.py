from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('',
    #/weatherapp
    url(r'^$', views.index, name='index'),
    url(r'^kmeans/$', views.kmeans, name='kmeans'),
    url(r'^kmeanspp/$', views.kmeanspp, name='kmeanspp'),
    url(r'^kmedoids/$', views.kmedoids, name='kmedoids'),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
