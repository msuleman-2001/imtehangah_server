import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models

from .role_enum import RoleEnum


class BaseUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, default="Unknown")
    last_name = models.CharField(max_length=50, default="Unknown")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=128, default=make_password("default_password"))

    user_type = models.CharField(max_length=50, choices=RoleEnum.choices(), default=RoleEnum.STUDENT.value)

    # Fixing the reverse accessor conflict
    groups = models.ManyToManyField(Group, related_name="baseuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="baseuser_permissions", blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.user_type == RoleEnum.ADMIN.value:
            group = Group.objects.get_or_create(name="Admin")
        elif self.user_type == RoleEnum.TEACHER.value:
            group = Group.objects.get_or_create(name="Teacher")
        else:
            group = Group.objects.get_or_create(name="Student")

        self.groups.set([group])

    def __str__(self):
        return f"{self.first_name}{self.last_name} - {self.email}"


# Student Model
class Student(BaseUser):
    student_roll_no = models.CharField(max_length=50, unique=True)
    groups = models.ManyToManyField(Group, related_name="student_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="student_permissions", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Student"


# Teacher Model
class Teacher(BaseUser):
    groups = models.ManyToManyField(Group, related_name="teacher_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="teacher_permissions", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Teacher"


# QuestionCategory Model
class QuestionCategory(models.Model):
    question_category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_category_name = models.CharField(max_length=100)
    is_enable = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='question_category_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='question_category_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question_category_name


# Question Model
class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice Question'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
    ]

    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.TextField()
    answers = models.JSONField()  # Stores array of answers
    correct_answers = models.JSONField()  # Stores array of correct answers
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name='questions')
    question_level = models.CharField(max_length=50)
    is_enable = models.BooleanField(default=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='questions_created')
    updated_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='questions_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question_text


# Examination Model
class Examination(models.Model):
    examination_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examination_name = models.CharField(max_length=100)
    number_of_questions = models.IntegerField()
    level = models.CharField(max_length=50)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name='examinations')
    pass_key = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    margin_time = models.IntegerField()  # Margin time in minutes
    is_enable = models.BooleanField(default=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='examinations_created')
    updated_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='examinations_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.examination_name


# StudentParticipation Model
class StudentParticipation(models.Model):
    student_participation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='participations')
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='participations')
    join_date_time = models.DateTimeField(auto_now_add=True)
    submit_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.student_name} - {self.examination.examination_name}"


# StudentResult Model
class StudentResult(models.Model):
    student_result_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participation = models.ForeignKey(StudentParticipation, on_delete=models.CASCADE, related_name='results')
    question_result = models.JSONField()  # Stores results of each question

    def __str__(self):
        return f"Result for {self.participation.student.student_name}"
