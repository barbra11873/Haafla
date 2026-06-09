from django.contrib import admin
from .models import HealthCheck


@admin.register(HealthCheck)
class HealthCheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')
