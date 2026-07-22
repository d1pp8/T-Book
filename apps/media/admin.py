from django.contrib import admin
from django.utils.html import format_html

from .models import Media, PropertyImage, UnitImage, UserAvatar, AmenityIcon


def thumbnail(field_name, label="Preview", height=60):
    """Build an admin readonly method that renders a small image preview."""
    def _thumb(self, obj):
        file = getattr(obj, field_name, None)
        if not file:
            return "—"
        try:
            url = file.url
        except ValueError:
            return "—"
        return format_html('<img src="{}" style="height:{}px;border-radius:4px;" />', url, height)
    _thumb.short_description = label
    return _thumb


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'preview', 'mime_type', 'size', 'width', 'height', 'created_at')
    list_filter = ('mime_type',)
    search_fields = ('original_name',)
    readonly_fields = ('uuid', 'preview', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    preview = thumbnail('file')


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('preview', 'property', 'is_cover', 'ordering', 'created_at')
    list_filter = ('is_cover',)
    search_fields = ('property__title',)
    autocomplete_fields = ('property',)
    readonly_fields = ('uuid', 'preview', 'created_at', 'updated_at')
    ordering = ('property', 'ordering')

    def preview(self, obj):
        if not obj.media_id or not obj.media.file:
            return "—"
        return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.media.file.url)
    preview.short_description = "Preview"


@admin.register(UnitImage)
class UnitImageAdmin(admin.ModelAdmin):
    list_display = ('preview', 'unit', 'is_cover', 'ordering', 'created_at')
    list_filter = ('is_cover',)
    search_fields = ('unit__title', 'unit__property__title')
    autocomplete_fields = ('unit',)
    readonly_fields = ('uuid', 'preview', 'created_at', 'updated_at')
    ordering = ('unit', 'ordering')

    def preview(self, obj):
        if not obj.media_id or not obj.media.file:
            return "—"
        return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.media.file.url)
    preview.short_description = "Preview"


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ('preview', 'user', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    autocomplete_fields = ('user',)
    readonly_fields = ('uuid', 'preview', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    def preview(self, obj):
        if not obj.media_id or not obj.media.file:
            return "—"
        return format_html('<img src="{}" style="height:60px;border-radius:50%;" />', obj.media.file.url)
    preview.short_description = "Preview"


@admin.register(AmenityIcon)
class AmenityIconAdmin(admin.ModelAdmin):
    list_display = ('preview', 'amenity', 'created_at')
    search_fields = ('amenity__title',)
    autocomplete_fields = ('amenity',)
    readonly_fields = ('uuid', 'preview', 'created_at', 'updated_at')
    ordering = ('amenity',)

    def preview(self, obj):
        if not obj.media_id or not obj.media.file:
            return "—"
        return format_html('<img src="{}" style="height:40px;" />', obj.media.file.url)
    preview.short_description = "Preview"