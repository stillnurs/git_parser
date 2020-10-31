from django.contrib import admin
from .models import *


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['url']
