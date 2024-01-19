from django.contrib import admin
from .models import SiteUser
# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    model = SiteUser
    list_display = (
        'email', 'password', 'username', 'last_login',
        'is_superuser', 'is_staff', 'is_active', 'date_joined'
    )
    search_fields = (
        'email', 'password', 'username', 'last_login',
        'is_superuser', 'is_staff', 'is_active', 'date_joined'
    )


admin.site.register(SiteUser, UsersAdmin)
