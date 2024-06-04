from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Region, City, SubCity

class Checkimpot(ImportExportModelAdmin, admin.ModelAdmin):
    # used easy import and export of the region model
    pass

admin.site.register(Region, Checkimpot)
admin.site.register(City, Checkimpot)
admin.site.register(SubCity, Checkimpot)
