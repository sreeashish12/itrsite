from django.urls import path,re_path
from . import views
urlpatterns = [
path('start', views.start, name='start'),
path('home',views.home,name='home'),
path('upload',views.upload,name='upload'),
path('table', views.table, name='table'),
re_path(r'^send/(?P<phone>[0-9]{12})/$', views.send,name='send'),
path("register", views.register_request, name="register") , 
path("login", views.login_request, name="login"),
path("logout", views.logout_request, name= "logout"),
path("", views.login_request, name="login"),
path("stats",views.stats,name="stats")
]