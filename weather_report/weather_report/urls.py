from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weather_report.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^weatherapp/', include('weatherapp.urls')),
    url(r'^$', include('weatherapp.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
