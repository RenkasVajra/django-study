from django.contrib import admin
from .models import Vacancy


# Register your models here.
class VacancyAdmin(admin.ModelAdmin):
    model = Vacancy
    list_display = ("title", 'description', 'skills', 'company', 'salary', 'area_name', 'published_at')
    search_fields = ("title", 'skills', 'company', 'salary', 'area_name', 'published_at')


admin.site.register(Vacancy, VacancyAdmin)
