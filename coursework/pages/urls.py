from django.urls import path
from . import views 


urlpatterns = [
    path('', views.main, name='main'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('documents/<int:document_id>/', views.documents, name='documents'),
]