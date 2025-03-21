from rest_framework import serializers

from .models import BaseUser, Student


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BaseUser
        fields = [  # Define fields in the same order as in your model
            'id', 'first_name', 'last_name', 'email', 'phone', 'department','username',
            'is_staff', 'is_superuser', 'is_active', 'user_type',
            'created_at', 'updated_at', 'remarks', 'password'
        ]


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_type = serializers.CharField(default="Student", read_only=True)

    class Meta:
        model = Student
        fields = [  # Define fields in the same order as in your model
            'id', 'first_name', 'last_name','username', 'email', 'phone', 'department', 'student_roll_no',
            'is_staff', 'is_superuser', 'is_active', 'user_type',
            'created_at', 'updated_at', 'remarks', 'password'
        ]


class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_type = serializers.CharField(default="Teacher", read_only=True)

    class Meta:
        model = BaseUser
        fields = [  # Define fields in the same order as in your model
            'id', 'first_name', 'last_name', 'email', 'phone', 'department',
            'is_staff', 'is_superuser', 'is_active', 'user_type',
            'created_at', 'updated_at', 'remarks', 'password'
        ]