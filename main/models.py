# ---------------------------
# 1. Importing necessary modules
# ---------------------------

from django.db import models
from django.contrib.auth.models import AbstractUser  # Import AbstractUser to extend the default User model
from django.utils import timezone  # Import timezone for handling time-based fields


# ---------------------------
# 2. Custom User Model
# ---------------------------

# We extend Django's AbstractUser to add custom roles (customer/admin) and additional fields
class User(AbstractUser):
    # A boolean to separate regular customers from admin users
    is_customer = models.BooleanField(default=True)
    
    # Custom password field with a maximum length of 8 characters
    password = models.CharField(max_length=8)
    
    # Custom field for customer name, it can be left blank or null
    customer_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        # Display the customer_name if available, else display the username
        return self.customer_name if self.customer_name else self.username


# ---------------------------
# 3. Food Item Model
# ---------------------------

# Represents a food item in the hotel menu
class FoodItem(models.Model):
    # The name of the food item (e.g., "Pizza", "Burger", etc.)
    name = models.CharField(max_length=100)
    
    # A short description of the food item
    description = models.TextField()
    
    # The price of the food item (e.g., 9999.99)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Category for grouping food items (e.g., Drinks, Main Dish, Snacks)
    category = models.CharField(max_length=50)
    
    # Field to upload images of the food item
    image = models.ImageField(upload_to='food_images/')
    
    # Boolean to indicate if the food is currently available
    is_available = models.BooleanField(default=True)

    def __str__(self):
        # Display the name of the food item
        return self.name


# ---------------------------
# 4. Room Model
# ---------------------------

# Represents the different room types in the hotel
class Room(models.Model):
    # Choices for room types
    ROOM_TYPE = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
        ('Deluxe', 'Deluxe'),
        ('Family', 'Family'),
        ('Presidential', 'Presidential'),
    ]
    
    # Choices for room booking status
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )
    
    # Room number as a unique identifier
    room_number = models.CharField(max_length=100)
    
    # Room type selection with available choices
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE)
    
    # Availability of the room (True if available, False if not)
    is_avilable = models.BooleanField(default=True)
    
    # Price per night for the room
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Image field for the room's picture
    room_image = models.ImageField(upload_to='room_images/')
    
    # Description of the room
    description = models.TextField()

    def __str__(self):
        # Return a string that combines room number and type for easy identification
        return f"{self.room_number} - {self.room_type}"


# ---------------------------
# 5. Booking Model
# ---------------------------

# Represents a booking made by a user for a specific room
class Booking(models.Model):
    # ForeignKey to User model to link a booking to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # ForeignKey to Room model to link a booking to a specific room
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    # Check-in and check-out dates for the booking
    check_in = models.DateField()
    check_out = models.DateField()
    
    # Date and time the booking was made
    booked_at = models.DateTimeField(auto_now_add=True)
    
    # Room type for the booking (default is 'single', options come from Room.ROOM_TYPE)
    room_type = models.CharField(max_length=100, default='single', choices=Room.ROOM_TYPE)
    
    # Booking status (default is 'Pending')
    status = models.CharField(max_length=100, default='Pending')

    # Removed redundant customer details from the Booking model
    # customer_name = models.CharField(max_length=100, default='customer_name')  # No longer needed
    # customer_email = models.EmailField(default='customer_email')  # No longer needed
    # customer_phone = models.CharField(max_length=10, default='customer_phone')  # No longer needed

    def __str__(self):
        # Display user customer name and booked room type
        return f"{self.user.customer_name} Booked {self.room.room_type}"


# ---------------------------
# 6. Order Model
# ---------------------------

# Represents a customer's food order
class Order(models.Model):
    # Status options for the order
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    # ForeignKey to User model to associate the order with a customer
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    
    # ForeignKey to FoodItem model to specify which food item was ordered
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    
    # Quantity of food items ordered
    quantity = models.PositiveIntegerField(default=1)
    
    # Time when the order was placed
    order_time = models.DateTimeField(default=timezone.now)
    
    # The current status of the order
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Optional: Delivery location or table number
    delivery_location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        # Show the customer name, food item, and the order status
        return f"{self.customer.customer_name} - {self.food_item.name} ({self.status})"

