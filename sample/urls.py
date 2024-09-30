# sample/urls.py
from django.urls import path
from . import views
from .views import SampleDetailView
app_name = 'sample'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('sample/add/', views.add_sample, name='add_sample'),
    path('samall/sample/', views.all_samples, name='all_samples'),
    path('sample/<int:pk>/', SampleDetailView.as_view(), name='sample_detail'),
    path('generate-certificate/<int:sample_id>/', views.generate_certificate, name='generate_certificate'),
    path('update_sample/<int:sample_id>/', views.update_sample, name='update_sample'),
    path('delete/<int:sample_id>/', views.delete_sample, name='delete_sample'),

]
