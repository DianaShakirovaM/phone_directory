from django.urls import path
from . import views

app_name = 'directory'

urlpatterns = [
    path('', views.PhoneDirectoryView.as_view(), name='phone_directory'),
    path(
        'employee/save/',
        views.EmployeeCreateUpdateView.as_view(),
        name='save_employee'
    ),
    path(
        'employee/delete/<int:employee_id>/',
        views.EmployeeDeleteView.as_view(),
        name='delete_employee'
    ),
    path('import/', views.import_data, name='import_data'),
    path('export/', views.DataExportView.as_view(), name='export_data'),
]
