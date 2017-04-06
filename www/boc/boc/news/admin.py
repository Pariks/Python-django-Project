from news.models import Article
from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, ArticleAdmin)
