from django.contrib import admin
from django.urls import path, include
from news_api import views  # Replace with your app name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('search/', views.search_news, name='search_news'),
   
]
