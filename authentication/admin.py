from django.contrib import admin
from .models import UserProfile, Officer, Supervisor

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_no']
    search_fields = ['user__username', 'phone_no']


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'is_on_duty', 'supervisor_no', 'get_user_profile_phone_no','duty_coord_lat', 'duty_coord_long', 'radius_of_duty']
    search_fields = ['user_profile__user__username', 'supervisor_no']
    list_filter = ['is_on_duty']

    def get_user_profile_phone_no(self, obj):
        return obj.user_profile.phone_no


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'get_user_profile_phone_no']
    search_fields = ['user_profile__user__username']

    def get_user_profile_phone_no(self, obj):
        return obj.user_profile.phone_no
