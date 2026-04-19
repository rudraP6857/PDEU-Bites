from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Base_App.views import *
from Base_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('signup/', SignupView, name='signup'),
    path('edit-profile/', EditProfileView, name='edit_profile'),

    # Pages
    path('', HomeView, name='Home'),
    path('book_table/', BookTableView, name='Book_Table'),
    path('menu/', MenuView, name='Menu'),
    path('about/', AboutView, name='About'),
    path('feedback/', FeedbackView, name='Feedback_Form'),

    # Cart AJAX
    # urls.py
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('get-cart-items/', views.get_cart_items, name='get_cart_items'), # Fix: JS calls /get-cart-items/
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout
    path('checkout/', checkout, name='checkout'),
    path('checkout-abandoned/', checkout_abandoned, name='checkout_abandoned'),
    path('order-history/', OrderHistoryView, name='order_history'),
    path('dashboard/', ManagerDashboardView, name='manager_dashboard'),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('order-success/<int:order_id>/', order_success, name='order_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)