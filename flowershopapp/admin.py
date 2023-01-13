from django.contrib import admin

from .models import User, Category, Bouquet, Order


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('name', 'phone_number')

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    search_fields = ('name', 'price', 'category')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('date_time', 'customer', 'delivery_date_time')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
