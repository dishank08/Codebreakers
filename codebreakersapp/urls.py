
from django.urls import path
from CodeBreakersapp.views import *
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', index),    
url(r'^login/$', login),
url(r'^logout/$', logout),
url(r'^auth/$', auth_view),
url(r'^home/$',home),
url(r'^addstudentinfo/$', views.addstudentinfo),
url(r'^register/$', views.register),
url(r'^practice/$', views.practice),
url(r'^profile/$', views.profile),
url(r'^editprofile/$', views.editprofile),
url(r'^update/$', views.update),
url(r'^leaderboard/$', views.leaderboard),
url(r'^execute/$',views.execute),
url(r'^code/$',views.code),
url(r'^contact/$',views.contact),
url(r'^feedback/$',views.feedback),
url(r'^addQuestion/$',views.addQuestion),
url(r'^users/$',views.users),
url(r'^userdelete/$',views.userdelete),
url(r'^deleteq/$',views.deleteq),
url(r'^add/$',views.add),
url(r'^practice/hcode/$',views.hcode),
url(r'^forgotpass/$',forgotpass),
url(r'^passverification/$',passverification),
url(r'^google8e6a172d6bdd9071.html/$',google),
url(r'^sitemap.xml/$',sitemap),
]
