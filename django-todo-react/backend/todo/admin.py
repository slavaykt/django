from django.contrib import admin
from .models import Todo, Step, Status

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')

# Register your models here.

admin.site.register(Todo, TodoAdmin)
admin.site.register(Step)
admin.site.register(Status)
