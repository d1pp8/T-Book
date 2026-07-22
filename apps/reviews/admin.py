from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'rating', 'booking', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = (
        'property__title',
        'user__email',
        'user__first_name',
        'user__last_name',
        'comment',
    )
    autocomplete_fields = ('user', 'booking', 'property')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    ordering = ('-created_at',)