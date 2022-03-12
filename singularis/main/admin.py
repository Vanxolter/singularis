from django.contrib import admin

from main.models import Airports


@admin.register(Airports)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ("name",)
    search_fields = ("name",)