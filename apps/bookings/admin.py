from django.contrib import admin

from .models import Booking, BookingGuest


class BookingGuestInline(admin.TabularInline):
    model = BookingGuest
    extra = 0
    fields = ('first_name', 'last_name', 'type', 'phone', 'email')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = [BookingGuestInline]

    list_display = (
        '__str__',
        'user',
        'unit',
        'status',
        'check_in',
        'check_out',
        'adults',
        'children',
        'total_price',
        'is_deleted',
    )
    list_filter = ('status', 'is_for_self', 'is_deleted', 'check_in', 'check_out')
    search_fields = (
        'unit__title',
        'unit__property__title',
        'user__email',
        'user__first_name',
        'user__last_name',
    )
    autocomplete_fields = ('user', 'unit')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    date_hierarchy = 'check_in'
    actions = ['restore_selected']

    def get_queryset(self, request):
        return Booking.all_objects.get_queryset()

    @admin.action(description="Restore selected bookings")
    def restore_selected(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)


@admin.register(BookingGuest)
class BookingGuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'type', 'phone', 'email', 'booking')
    list_filter = ('type',)
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'booking__unit__title')
    autocomplete_fields = ('booking',)