from django.contrib import admin

from .models import SubscriptionInfo, Benefit, ScheduleConsultation

class SubscriptionInfoAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,  {'fields' : ['duration']}),
            ('Price Information', {'fields' : ['price']}),
        ]

class ScheduleConsultationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')

admin.site.register(SubscriptionInfo, SubscriptionInfoAdmin)
admin.site.register(Benefit)
admin.site.register(ScheduleConsultation, ScheduleConsultationAdmin)

