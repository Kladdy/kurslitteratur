from django.contrib import admin

# Register your models here.

from .models import Book, University, Programme, Semester, Course

admin.site.register(Book)
admin.site.register(University)
admin.site.register(Programme)
admin.site.register(Semester)
admin.site.register(Course)