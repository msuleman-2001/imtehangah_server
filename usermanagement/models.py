import uuid

from django.contrib.auth.models import User
from django.db import models


# Student Model
class Student(models.Model):
    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_roll_no = models.CharField(max_length=50, unique=True)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_phone = models.CharField(max_length=15)
    student_password = models.CharField(max_length=128)
    is_enable = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='student_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='student_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.student_name


# Teacher Model
class Teacher(models.Model):
    teacher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher_name = models.CharField(max_length=100)
    teacher_email = models.EmailField(unique=True)
    teacher_phone = models.CharField(max_length=15)
    teacher_password = models.CharField(max_length=128)
    is_enable = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teacher_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teacher_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.teacher_name


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
