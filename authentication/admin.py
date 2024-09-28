from django.contrib import admin
from .models import UserProfile, Officer, Supervisor

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_no')
    search_fields = ('user__username', 'phone_no')

class OfficerAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'is_on_duty', 'supervisor_no', 'user_profile_phone_no')
    search_fields = ('user_profile__user__username', 'supervisor_no')
    list_filter = ('is_on_duty',)

    def user_profile_phone_no(self, obj):
        return obj.user_profile.phone_no
    user_profile_phone_no.short_description = 'Phone Number'

class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'user_profile_phone_no')
    search_fields = ('user_profile__user__username',)

    def user_profile_phone_no(self, obj):
        return obj.user_profile.phone_no
    user_profile_phone_no.short_description = 'Phone Number'

# Register your models here
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Officer, OfficerAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
