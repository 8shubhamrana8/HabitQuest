from django.contrib import admin
from .models import User, Rank, DailyLog, Habit, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Rank)
admin.site.register(DailyLog)
admin.site.register(Habit)
admin.site.register(Comment)