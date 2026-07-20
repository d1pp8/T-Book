from django.contrib import admin
from django.utils.html import format_html
from django import forms
from apps.media.services import AmenityIconService
from .models import Property, Unit, Bed, Amenity

class AmenityAdminForm(forms.ModelForm):
    icon_file = forms.ImageField(required=False, label="Icon")

    class Meta:
        model = Amenity
        fields = ('title',)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    form = AmenityAdminForm
    list_display = ('title', 'icon_preview',)
    search_fields = ('title',)

    def icon_preview(self, obj):
        icon = getattr(obj, "icon", None)
        if icon:
            return format_html('<img src="{}" style="height:24px" />', icon.media.file.url)
        return "—"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        uploaded_file = form.cleaned_data.get('icon_file')
        if uploaded_file:
            AmenityIconService.upload(obj, uploaded_file)



class BedInline(admin.TabularInline):
    model = Bed
    extra = 1

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    show_change_link = True


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [UnitInline]
    list_display = (
        'title',
        'owner',
        'type',
        'status',
        'city',
        'country',
        'rating',
        'created_at',
    )
    list_filter = ('type', 'status', 'country', 'city',)
    search_fields = (
        'title',
        'description',
        'city',
        'country',
        'street',
        'owner__email',
    )
    autocomplete_fields = ('owner',)
    filter_horizontal = ('amenities',)
    readonly_fields = ('uuid', 'rating', 'created_at', 'updated_at',)
    ordering = ('-created_at',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    inlines = [BedInline]
    list_display = (
        '__str__',
        'property',
        'status',
        'price_per_night',
        'max_guests',
        'bedrooms',
        'bathrooms',
        'room_number'
    )
    list_filter = ('status', 'property__type')
    search_fields = ('title', 'description', 'property__title', 'room_number')
    autocomplete_fields = ('property',)
    filter_horizontal = ('amenities',)
    readonly_fields = ('uuid', 'created_at', 'updated_at',)
    ordering = ('property', 'room_number',)


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('unit', 'bed_type', 'quantity')
    list_filter = ('bed_type',)
    search_fields = ('unit__title','unit__property__title')
    autocomplete_fields = ('unit',)