from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Contact, Donation, FoodRequest, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "contact_number", "address")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"classes": ("wide",), "fields": ("role", "contact_number", "address")}),
    )
    list_display = ("username", "email", "role", "contact_number")
    list_filter = ("role",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("food_name", "donor", "status", "available_till")
    list_filter = ("status", "available_till")
    search_fields = ("food_name", "donor__username", "donor__email")


@admin.register(FoodRequest)
class FoodRequestAdmin(admin.ModelAdmin):
    list_display = ("donation", "receiver", "status", "timestamp")
    list_filter = ("status", "timestamp")
    search_fields = ("donation__food_name", "receiver__username", "receiver__email")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
