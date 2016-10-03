from django.conf.urls import url, include
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<item_id>\d+)/$' , views.detail, name='detail'),
        url(r'^about/$', views.about, name="about"),
        url(r'^suggestions/$', views.suggestions, name="suggestions"),
        url(r'^suggestion/(?P<item_id>\d+)/$', views.suggestion, name="suggestion"),
        url(r'^newitem/$', views.newitem, name="newitem"),
        url(r'^searchlib/$',views.searchlib, name='searchlib'),
        url(r'^login/$',views.user_login,name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^myitem/$', views.myitems, name='myitem'),
        url(r'^forgot/$', views.forgot_password, name='forgot'),
        url(r'^register/$', views.register, name='register'),
        url(r'^success/$', views.success, name='success'),
        url(r'^profile/$', views.profile, name='profile')
        ]
