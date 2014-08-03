from django.conf.urls import patterns, url


urlpatterns = patterns(
    'lists.views',
    url(
        r'^(\d+)/$', 'view_list',
        name='view_list'
    ),
    url(
        r'^(\d+)/new_item$', 'add_item',
        name='add_item'
    ),
    url(r'^new$', 'new_list', name='new_list'),
)
