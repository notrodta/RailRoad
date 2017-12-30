from django.conf.urls import url
from . import views

app_name = 'turk'

urlpatterns = [

    url(r'^front_page/$', views.front_page, name='front_page'),
    url(r'^reservation/(?P<stop_id>[0-9]+)/train/(?P<train_id>[0-9]+)/seg/(?P<seg_id>[0-9]+)/des/(?P<des_id>[0-9]+)/(?P<date>\d{4}-\d{2}-\d{2})/$', views.reservation, name='reservation'),
    url(r'^cancellation/$', views.cancellation, name='cancellation'),
    #url(r'^rebook/$', views.rebook, name='rebook'),
    url(r'^createdb/$', views.createdb, name='createdb'),
    url(r'^confirm_cancellation/$', views.confirm_cancellation, name='confirm_cancellation'),
    url(r'^confirm_reservation/pass/(?P<pass_id>[0-9]+)/res/(?P<res_id>[0-9]+)/stop/(?P<stop_id>[0-9]+)/trip/(?P<trip_id>[0-9]+)/$', views.confirm_reservation, name='confirm_reservation'),


    # update profile page
   # url(r'^profile/(?P<user_id>[0-9]+)/UpdateProfile/(?P<pk>[0-9]+)$', views.UpdateProfile.as_view(),
    #    name='update_profile'),

]