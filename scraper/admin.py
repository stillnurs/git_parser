from django.contrib import admin
from .models import *


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']


@admin.register(Commits)
class CommitsAdmin(admin.ModelAdmin):
    list_display = ['title', 'message', 'timestamp', 'date']
