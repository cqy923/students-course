from django.contrib import admin

from .models import Course,StudentCourse,Schedule

admin.site.register(Schedule)
admin.site.register(Course)
admin.site.register(StudentCourse)
