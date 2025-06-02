# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class UserProfileInline(admin.StackedInline): # or admin.TabularInline
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_select_related = ('profile', )

    def get_role(self, instance):
        return instance.profile.get_role_display()
    get_role.short_description = 'Role'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(CustomUser._meta.get_field('groups').remote_field.model) # If you are not using Django's groups
admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserProfile) # Optional: if you want to manage profiles separately as well