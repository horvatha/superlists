from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
)
