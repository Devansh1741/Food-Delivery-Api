from django.contrib import admin
from .models import Restaurant, Dish, User, Order

# Register your models here.

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    # Customize how Restaurant objects are displayed in the admin
    list_display = ('restaurant_id', 'name', 'address',)
    search_fields = ('name', 'address',)
    # Make restaurant_id read-only as it's generated by UUID
    readonly_fields = ('restaurant_id',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    # Customize how Dish objects are displayed in the admin
    list_display = ('dish_id', 'name', 'restaurant_id', 'price', 'is_available',)
    list_filter = ('is_available', 'restaurant_id',)
    search_fields = ('name', 'description',)
    # Make dish_id read-only as it's generated by UUID
    readonly_fields = ('dish_id',)
    raw_id_fields = ('restaurant_id',) # Use a raw ID field for ForeignKey to improve performance for many restaurants

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Customize how User objects are displayed in the admin
    list_display = ('user_id', 'name', 'phone_number',)
    search_fields = ('name', 'phone_number',)
    # Make user_id read-only as it's generated by UUID
    readonly_fields = ('user_id',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Customize how Order objects are displayed in the admin
    list_display = ('order_id', 'user', 'restaurant_id', 'total_amount', 'payment_type', 'status',)
    list_filter = ('status', 'payment_type', 'restaurant_id',)
    search_fields = ('order_id', 'user__name', 'restaurant__name',)
    # Make order_id, total_amount, and status read-only as they are set programmatically
    readonly_fields = ('order_id', 'total_amount',)
    raw_id_fields = ('user', 'restaurant_id', 'items',) # Use raw ID fields for ForeignKeys and ManyToMany to improve performance
