from django.contrib import admin
from investor.models import Investor, InvestorRelation

# Register your models here.

admin.site.register(Investor)
admin.site.register(InvestorRelation)