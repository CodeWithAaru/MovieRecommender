from django.contrib import admin
from django.urls import path
from Rating import views

urlpatterns = [
    path("",views.index , name = 'Form'),
    path("submitData",views.submitData, name = 'submitData'),
    path("add_movie",views.add_movie,name='add_movie'),
    path("AddMovieName",views.AddMovieName,name='AddMovieName'),
    path("recommend_movie",views.recommend_movie,name='recommend_movie'),
    path("recommend_movie_display",views.recommend_movie_display,name='recommend_movie_display'),
    path("redirect_to_rate",views.redirect_to_rate,name='redirect_to_rate'),
    path("add_user",views.add_user,name='add_user'),
    path("AddUserName",views.AddUserName,name='AddUserName'),
    path('find_movie',views.find_movie,name='find_movie')
    
    
]