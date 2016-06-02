from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^doc/$', RedirectView.as_view(url='/python_doc/index.html')),
    url(r'^lists/', include('lists.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
