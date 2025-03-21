from rest_framework import generics

from .models import BaseUser, Student, Teacher
from .serializers import BaseUserSerializer, StudentSerializer, TeacherSerializer


# Create your views here.
class UserListCreateView(generics.ListCreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer


class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.all()


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.all()


class TeacherListCreateView(generics.ListCreateAPIView):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.all()


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.all()
