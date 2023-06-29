from django.contrib import admin
from .models import Customer, Stone, StoneItem


class StoneItemAdmin(admin.TabularInline):
    model = StoneItem
    extra = 0


@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):

    class Meta:
        model = Stone


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [StoneItemAdmin]

    class Meta:
        model = Customer
