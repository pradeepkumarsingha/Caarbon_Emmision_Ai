from django.urls import path
from . import views

app_name = 'windsurf'

urlpatterns = [
    path('', views.home, name='home'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('events/', views.event_list, name='event_list'),
    path('blog/', views.blog_list, name='blog_list'),
    path('contact/', views.contact, name='contact'),
    path('predict/', views.predict_emissions, name='predict_emissions'),
]
