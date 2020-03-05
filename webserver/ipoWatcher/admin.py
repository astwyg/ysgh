from django.contrib import admin

from .models import *


@admin.register(Watcher)
class WatcherAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "keywords", "threshold", "available")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "link", "checked", "downloaded")