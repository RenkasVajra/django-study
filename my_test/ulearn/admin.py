from django.contrib import admin
from .models import Vacancy, Demand, Geography


# Register your models here.
class VacancyAdmin(admin.ModelAdmin):
    model = Vacancy
    list_display = ('title', 'description', 'skills', 'company', 'salary', 'area_name', 'published_at')
    search_fields = ('title', 'skills', 'company', 'salary', 'area_name', 'published_at')


class DemandAdmin(admin.ModelAdmin):
    model = Demand
    list_display = ('title', 'image', 'table')
    search_fields = ('title',)


class GeographyAdmin(admin.ModelAdmin):
    model = Demand
    list_display = ('title', 'image', 'table')
    search_fields = ('title',)


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Demand, DemandAdmin)
admin.site.register(Geography, GeographyAdmin)
