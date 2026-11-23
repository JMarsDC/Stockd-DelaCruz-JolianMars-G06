from django.contrib import admin

from .models import Item, Storage


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "storage_type", "created_at"]
    list_filter = ["storage_type"]
    search_fields = ["name", "owner__username"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "storage", "owner", "quantity", "unit", "expiry_date"]
    list_filter = ["unit"]
    search_fields = ["name", "storage__name", "owner__username"]