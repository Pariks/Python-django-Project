from bookmakers.models import Bookmaker, Banner, BookmakerHead
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from ckeditor.widgets import CKEditorWidget

# Register your models here.


class BookmakerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
    

admin.site.register(Bookmaker, BookmakerAdmin)
admin.site.register(Banner)
admin.site.register(BookmakerHead)


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)