from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category


class Checkimpot(ImportExportModelAdmin, admin.ModelAdmin):
    # used easy import and export of the region model
    pass

admin.site.register(Category, Checkimpot)