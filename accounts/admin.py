from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["first_name", "last_name", "username", "email", "role", "is_staff"]
    list_filter = ["role", "is_staff", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role", "contact_number")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("email", "role", "contact_number")}),
    )