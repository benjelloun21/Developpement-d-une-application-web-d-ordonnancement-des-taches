from django.contrib import admin
from .models import task
from django.contrib.auth.models import Group

admin.site.site_header='IO Dashboard'

class taskAdmin(admin.ModelAdmin):
    list_display=('Attribute','Task','Duration','Predecessors','EarliestST','LatestST','tfloat','ffloat','RequiredRT','EstimatedEf','Staffid','Progress')
    list_filter=['RequiredRT']
admin.site.register(task,taskAdmin)


