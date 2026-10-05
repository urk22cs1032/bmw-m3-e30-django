from django.contrib import admin

from showroom.models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """The CRUD surface for the collection grid.

    Search and filter here mirror the ones on the public page exactly — same
    four fields, same status choices — so an administrator can find a record
    by whatever term they would have typed into the collection search box.
    """

    list_display = (
        "bmw_id",
        "model",
        "year",
        "variant",
        "status",
        "price",
        "has_image",
    )
    list_editable = ("status",)
    list_filter = ("status", "year")
    search_fields = ("bmw_id", "model", "variant", "customer_name", "registration_number")
    ordering = ("-created_at", "-pk")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("bmw_id", "model", "year", "variant")}),
        ("Sale", {"fields": ("price", "status")}),
        ("Customer", {"fields": ("customer_name", "registration_number")}),
        ("Media", {"fields": ("image",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(boolean=True, description="Photo")
    def has_image(self, obj):
        return bool(obj.image)
