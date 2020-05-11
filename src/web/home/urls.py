from django.urls import include, path
from django.conf.urls import url
from . import views
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.index, name='index'),
    path('getvmlist', views.getvmlist, name='get_vm_list'),
    path('getresources', views.user_groups, name='user_groups'),
    path('detail', views.get_detail, name='get_detail'),
    path('groups', views.group_list, name='group_list'),
    url(r'^groups/create/$', views.group_create, name='group_create'),
    url(r'^groups/(?P<pk>\d+)/update/$', views.group_update, name='group_update'),
    url(r'^groups/(?P<pk>\d+)/delete/$', views.group_delete, name='group_delete'),

    url(r'^detail/(?P<pk>.+)/start/$', views.vm_start, name='vm_start'),
    url(r'^detail/(?P<pk>.+)/stop/$', views.vm_stop, name='vm_stop'),
    url(r'^detail/(?P<pk>.+)/restart/$', views.vm_restart, name='vm_restart'),
]