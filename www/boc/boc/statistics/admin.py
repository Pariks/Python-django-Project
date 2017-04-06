from django.contrib import admin
from statistics.models import Statistic, StatisticsContent
from django.db import models
from ckeditor.widgets import CKEditorWidget

# Register your models here.


class StatisticsContentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

# Register your models here.

admin.site.register(Statistic)
admin.site.register(StatisticsContent, StatisticsContentAdmin)