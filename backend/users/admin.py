from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
# Register your models here.




class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'photo', 'data_birth')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined' , 'last_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'photo'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'data_birth')  # Указываем, что хотим видеть в списке
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)

