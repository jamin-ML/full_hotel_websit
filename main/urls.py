# A ding to root so that the be accessed from the root
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('food/', views.food_menu, name='food_menu'),
    path('about/',views.about, name='about'),  # Added about view to root
    path('rooms/', views.rooms, name='rooms'),
    path('book/', views.book_room, name='book_room'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('register/', views.register_form, name='register'),
    path('login/', views.login_view, name='login'),
    path('book-room/', views.book_room, name='book_room'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', views.search_results, name='search_results'),
    path('order/<int:food_id>/', views.order_food, name='order_food'),

    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
