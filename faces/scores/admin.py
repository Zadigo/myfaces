from django.contrib import admin

from scores.models import Face, Score, UserDetail


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['image', 'numeric', 'emotion']
    date_hierarchy = 'created_on'


@admin.register(Face)
class FaceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'skin_color']
    list_per_page = 30


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ['session', 'country', 'gender']
    list_per_page = 30
