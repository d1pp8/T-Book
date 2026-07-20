from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User
    ordering = ('email',) 
    
    list_display = (
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
    )

    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': (
                'first_name',
                'last_name',
                'avatar',
                'birth_date',
                'phone',
                'sex',
                'citizenship'
                )
        }),
        ('Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login',
                'created_at'
            )
        })
    )


    add_fieldsets = (
        (None, 
         {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_superuser'
            ),
        },
        ),
    )