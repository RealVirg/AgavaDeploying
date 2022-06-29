from django.urls import path
from . import views


urlpatterns = [
    path('', views.account, name='account'),
    path('<int:id>', views.project, name="project-detail"),
    path('<int:id>/admin/', views.admin, name='admin'),
    path('<int:id>/devices/', views.devices, name='devices'),
    path('devices/<int:id>', views.device, name='device'),
    path('<int:id>/monitors', views.monitors, name='monitors'),
    path('<int:id>', views.monitor, name='monitor')
]
