from django.urls import path
from . import views

# index is always the root route
urlpatterns = [
	path('', views.index),
    path('register',views.register),
    # rule of thumb, when sending form or post data to a route in server ,you must redirect
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout)
]