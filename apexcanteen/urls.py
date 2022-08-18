from tkinter import Menu
from django.urls import path
from . import views
urlpatterns = [
    
    path('home',views.home),
    path('about',views.about),
    path('product',views.product),
    path('login',views.login),

    # path('menu',views.menu),
    # path('test',views.test),
   
    # path('llogin',views.llogin),
]
