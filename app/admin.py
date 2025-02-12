from django.contrib import admin
from .models import Lista_tarefas
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(Lista_tarefas)


class Lista_tarefasAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'done', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'done', 'created_at', 'updated_at')

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'Aditional Info',
            {
                'fields': (
                    'profile_picture',
                ),
            },
        ),
    )
admin.site.register(CustomUser, CustomUserAdmin)