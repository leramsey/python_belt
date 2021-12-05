from django.urls import path
from . import views

urlpatterns = [
    path('main', views.main, name="main"), #register and login
    path('friends', views.friends, name="friends"), #two tables
    path ('user/<int:id>', views.view_profile, name="view_profile"),
    path ('register', views.register, name="register"),
    path ('login', views.login, name="login"),
    path ('add_friend/<int:fid>', views.add_friend, name="add_friend"),
    path ('remove_friend/<int:fid>', views.remove_friend, name="remove_friend"),
    path ('logout', views.logout, name="logout"),
    
]