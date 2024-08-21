from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Attendance, ReferencePoint

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('department', 'phone_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Attendance)


@admin.register(ReferencePoint)
class ReferencePointAdmin(admin.ModelAdmin):
    list_display = ('name', 'easting', 'northing')
