from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

UserAdmin.list_display = ('first_name', 'last_name', 'username', 'email', 'date_joined')
UserAdmin.ordering = ('-date_joined', )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
