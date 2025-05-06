from django.contrib import admin
from .models import FoodItem, Order, Booking, Room, User,About

# Site Customization
admin.site.site_header = "Hotel Management"
admin.site.site_title = "Hotel Admin"
admin.site.index_title = "Welcome to Hotel Admin Dashboard"
admin.site.enable_nav_sidebar = True  # Optional, hides the right sidebar

# Custom CSS for Admin Panel
class MyAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # Custom CSS file
        }

# Booking Admin Configuration
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'status')  # Fields to display
    list_filter = ('user', 'room', 'room_type', 'check_in', 'check_out', 'status')  # Fields for filtering
    search_fields = ('user__username', 'room__room_number')  # Fields for search
    list_editable = ('status',)  # Editable fields

# Register Booking model
admin.site.register(Booking, BookingAdmin)

# Order Admin Configuration
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'food_item', 'order_time', 'status')  # Fields to display
    list_filter = ('status', 'order_time')  # Fields for filtering
    search_fields = ('customer__username', 'food_item__name')  # Fields for search
    list_editable = ('status',)  # Editable fields

# Register Order model
admin.site.register(Order, OrderAdmin)

# User Admin Configuration
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_customer', 'customer_name')  # Add customer_name to list_display

# Register User model
admin.site.register(User, UserAdmin)

# Apply MyAdmin class to FoodItem and Room models for custom CSS
class FoodItemAdmin(MyAdmin):
    pass

class RoomAdmin(MyAdmin):
    pass

# Register FoodItem and Room models with custom admin
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Room, RoomAdmin)


class AboutAdmin(MyAdmin):
    list_display = ('title', 'description')  # Fields to display
admin.site.register(About, AboutAdmin)  # Register About model with custom admin
