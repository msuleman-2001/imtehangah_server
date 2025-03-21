from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('students/', views.StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<uuid:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('teachers/', views.TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('teachers/<uuid:pk>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
]