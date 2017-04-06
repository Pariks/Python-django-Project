from django.contrib import admin
from predictions.models import Prediction, PredictionArticle
from django.db import models
from ckeditor.widgets import CKEditorWidget

# Register your models here.


class PredictionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
    filter_horizontal = ('fight',)
    
class PredictionArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.register(Prediction, PredictionAdmin)
admin.site.register(PredictionArticle, PredictionArticleAdmin)