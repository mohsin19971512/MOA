from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'laboratory'
urlpatterns = [
    path('', views.lab_assigned_samples, name='lab_assigned_samples'),
    path('all/assignments/', views.all_assignments, name='all_assignments'),
    path('purity_test/create/<int:assignment_id>/', views.create_purity_test, name='create_purity_test'),
    path('purity_test/update/<int:assignment_id>/', views.update_purity_test, name='update_purity_test'),

    path('purity_test/details/<int:assignment_id>/', views.purity_test_detail, name='purity_test_detail'),

    path('moisture_test/details/<int:assignment_id>/', views.moisture_test_detail, name='moisture_test_detail'),
    path('moisture_test/create/<int:assignment_id>/', views.create_moisture_test, name='create_moisture_test'),
    path('moisture_test/<int:assignment_id>/update/', views.update_moisture_test, name='update_moisture_test'),

    path('plant_test/create/<int:assignment_id>/', views.create_plant_test, name='create_plant_test'),
    path('create_health_test/<int:assignment_id>/', views.create_health_test, name='create_health_test'),

    
]
