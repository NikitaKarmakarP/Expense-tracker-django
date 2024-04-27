from . import views
from django.urls import path 

urlpatterns = [
    path('', views.register),
    path('register' , views.register),
    path('regi' , views.regi),
    path('login' , views.login),
    path('logi' , views.logi),
    path('show' , views.show),
    path('addTransaction' , views.addTransaction),
    # path('editOrDelete' , views.editOrDelete),
    path('del/<int:id>' , views.delete_transaction),
    path('edit/<int:id>' , views.editTransaction),
    # path('welcome' , views.welcome)
    
]
