from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClientRequest, Event, Registration, Sponsorship, Review

# 1. Custom User Admin
# This ensures you can see and edit the 'role' field in the Admin panel
class CustomUserAdmin(UserAdmin):
    model = User
    # Display these columns in the list view
    list_display = ['username', 'email', 'role', 'is_staff']
    
    # Allow editing the 'role' field in the admin form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# 2. Register all models
admin.site.register(User, CustomUserAdmin)
admin.site.register(ClientRequest)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Sponsorship)
admin.site.register(Review)