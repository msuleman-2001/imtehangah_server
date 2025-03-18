from django.contrib import admin

from .models import Student, Teacher, QuestionCategory, Question, Examination, StudentParticipation, StudentResult

admin.site.register(Student)
admin.site.register(Teacher)

admin.site.register(QuestionCategory)
admin.site.register(Question)
admin.site.register(Examination)
admin.site.register(StudentParticipation)
admin.site.register(StudentResult)
