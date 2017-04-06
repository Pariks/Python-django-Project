from django.contrib import admin
from userprofile.models import UserExtraInfo, PhoneNumber

# Register your models here.

class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user',  'sent')


admin.site.register(UserExtraInfo)
admin.site.register(PhoneNumber, PhoneNumberAdmin)