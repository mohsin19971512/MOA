from django.urls import path
from . import views
from .Health.views import HealthTestDetailView, update_health_test, create_health_test
from .Moisture.views import moisture_test_detail, create_moisture_test, update_moisture_test
from .Plan.views import create_plant_test, update_plant_test
from .Purity.views import create_purity_test, update_purity_test, purity_test_detail

app_name = 'laboratory'
urlpatterns = [
    path('', views.lab_assigned_samples, name='lab_assigned_samples'),
    path('purity_test/create/<int:assignment_id>/', create_purity_test, name='create_purity_test'),
    path('purity_test/update/<int:assignment_id>/', update_purity_test, name='update_purity_test'),
    path('purity_test/details/<int:assignment_id>/', purity_test_detail, name='purity_test_detail'),

    path('moisture_test/details/<int:assignment_id>/', moisture_test_detail, name='moisture_test_detail'),
    path('moisture_test/create/<int:assignment_id>/', create_moisture_test, name='create_moisture_test'),
    path('moisture_test/<int:assignment_id>/update/', update_moisture_test, name='update_moisture_test'),

    path('plant_test/create/<int:assignment_id>/', create_plant_test, name='create_plant_test'),
    path('update_plant_test/<int:assignment_id>/', update_plant_test, name='update_plant_test'),
    path('health_test_details/<int:assignment_id>/', HealthTestDetailView.as_view(), name='health_test_detail'),

    path('create_health_test/<int:assignment_id>/', create_health_test, name='create_health_test'),

    path('update_health_test/<int:assignment_id>/', update_health_test, name='update_health_test'),
]

