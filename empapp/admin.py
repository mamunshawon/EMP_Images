from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(DailyTask)
admin.site.register(Leave)
admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(TodoList)
admin.site.register(PunchIn)