from django.urls import path

from . import views
urlpatterns = [
    path('', views.index_view, name='Dashboard-index'),
    path('staff/', views.staff_view, name='Dashboard-staff'),
    path('staff/detail/<int:pk>/', views.staff_detail, name='Dashboard-staff-detail'),
    path('tasks/', views.tasks_view, name='Dashboard-tasks'),
    path('critical_path/', views.critical_path_view, name='critical_path'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='Dashboard-tasks-delete'),
    path('tasks/update/<int:pk>/', views.task_update, name='Dashboard-tasks-update'),
    path('progress/', views.progress_view, name='Dashboard-progress'),
    ]