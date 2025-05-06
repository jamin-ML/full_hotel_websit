from django.shortcuts import render, redirect,get_list_or_404
from .models import FoodItem, Room, Booking, About
from django.contrib.auth.decorators import login_required
from .forms import BookingForm, RegisterForm, RegisterForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
# Home / Menu
def food_menu(request):
    food_items = FoodItem.objects.all()
    return render(request, 'main/food_menu.html', {'food_items': food_items})

def about(request):
    about_items = About.objects.all()
    return render(request, 'main/about.html', {'about_items': about_items}) 

def home(request):
    return redirect('food_menu')

# Room ordering
def rooms(request):
    rooms_items = Room.objects.all()
    return render(request, 'main/rooms.html', {'rooms_items': rooms_items})

# Booking
@login_required
def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'main/booking_form.html', {'form': form})

def booking_success(request):
    return render(request, 'main/booking_success.html')

# Registration
def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            email = form.cleaned_data['email']

            send_mail(
                'Welcome to Grand Hotel!',
                f'Hi {user.username}, thank you for creating an account with us!',
                'jumajamin55@gmail.com',
                [email],
                fail_silently=False,
            )

            auth_login(request, user)
            return redirect('food_menu')  # Log them in and redirect
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in the form correctly.')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def booking_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer_name = request.POST.get('customer_name')
            booking.customer_phone = request.POST.get('customer_phone')
            booking.customer_email = request.POST.get('customer_email')
            booking.save()
            messages.success(request,'Room succcessfuly abaooked!')
            return redirect('booking-success')
        
        else:
            return 'There was an error while submiting your form!'
        
    else:
        form.BookingForm()

    return render(request,'book_room.html',{'form': form})

from django.shortcuts import render
from .models import Room, FoodItem  # Make sure you import your actual food model
from django.db.models import Q

def search_results(request):
    query = request.GET.get('q')
    room_results = []
    food_results = []

    if query:
        room_results = Room.objects.filter(
            Q(description__icontains=query) |
            Q(room_type__icontains=query)
        )
        food_results = FoodItem.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'query': query,
        'room_results': room_results,
        'food_results': food_results,
    }
    return render(request, 'search_results.html', context)

def order_food(request, food_id):
    food_item = get_list_or_404(FoodItem, id=food_id)
    if request.method == 'POST':
        # Process the order here (e.g., save to database, send confirmation email, etc.)
        messages.success(request, f'Order for {food_item.name} has been placed successfully!')
        return redirect('food_menu')
    return render(request, 'order_food.html', {'food_item': food_item}) 
