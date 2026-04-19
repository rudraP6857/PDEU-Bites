from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Items, Order, OrderItem, ItemList, Feedback, BookTable, AboutUs
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# --- Page Views ---
def LogoutView(request):
    """
    Handles the user logout.
    1. Clears the session (and the cart).
    2. Logs the user out.
    3. Redirects to a 'logged out' confirmation page or home.
    """
    if request.method == "POST":
        logout(request)
        # You can redirect to a specific 'logged_out.html' or back to 'Home'
        return render(request, 'logged_out.html') 
    
    # If the user just navigates to the URL, show a confirmation page
    return render(request, 'logout_confirm.html')

def HomeView(request):
    items = Items.objects.all()
    list = ItemList.objects.all()
    review = Feedback.objects.all()
    return render(request, 'home.html', {'items': items, 'list': list, 'review': review})


def MenuView(request):
    query = request.GET.get('q')
    if query:
        items = Items.objects.filter(Item_name__icontains=query)
    else:
        items = Items.objects.all()
        
    list = ItemList.objects.all()
    return render(request, 'menu.html', {'items': items, 'list': list, 'query': query})

def AboutView(request):
    data = AboutUs.objects.all()
    return render(request, 'about.html', {'data': data})

def BookTableView(request):
    if request.method == "POST":
        name = request.POST.get('user_name')
        phone = request.POST.get('phone_number')
        email = request.POST.get('user_email')
        person = request.POST.get('total_person')
        date = request.POST.get('booking_data')
        time = request.POST.get('booking_time')
        request_text = request.POST.get('special_request')

        if name and email and date:
            BookTable.objects.create(
                Name=name,
                Phone_number=phone,
                Email=email,
                Total_person=person,
                Booking_date=date,
                Booking_time=time,
                Special_request=request_text
            )

            # Send Email
            try:
                subject = 'Table Booking Confirmation - PDEU Bites'
                message = f'Hi {name},\n\nYour table for {person} person(s) has been booked for {date} at {time}.\n\nSpecial Request: {request_text or "None"}\n\nWe look forward to serving you!\n\nRegards,\nPDEU Bites Team'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            except Exception as e:
                print(f"Email error: {e}")

            messages.success(request, 'Your table has been booked successfully!')
            return redirect('Book_Table')

    return render(request, 'book_table.html')

def FeedbackView(request):
    if request.method == "POST":
        name = request.POST.get('User_name')
        email = request.POST.get('User_email')
        rating = request.POST.get('Rating')
        description = request.POST.get('Description')
        image = request.FILES.get('Selfie')

        if name and description:
            Feedback.objects.create(
                User_name=name,
                Email=email,
                Rating=rating,
                Description=description,
                Image=image
            )

            # Send Email
            if email:
                try:
                    subject = 'Thank you for your feedback! - PDEU Bites'
                    message = f'Hi {name},\n\nThank you for your valuable feedback. We have received your {rating}-star rating.\n\nYour Feedback: "{description}"\n\nWe strive to improve every day based on your inputs.\n\nRegards,\nPDEU Bites Team'
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                except Exception as e:
                    print(f"Email error: {e}")

            messages.success(request, 'Thank you! Your feedback has been submitted successfully.')
            return redirect('Feedback_Form')

    return render(request, 'feedback.html')

def SignupView(request):
    # Add your signup logic here (e.g., UserCreationForm)
    return render(request, 'signup.html')

# --- Cart Logic ---

def add_to_cart(request):

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required'})
    
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Items, id=item_id)
        cart = request.session.get('cart', {})

        if item_id in cart:
            cart[item_id]['quantity'] += 1
        else:
            cart[item_id] = {
                'name': item.Item_name, 
                'price': float(item.Price), 
                'quantity': 1
            }
        
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'message': 'Added', 'cart_count': len(cart)})


def get_cart_items(request):
    cart = request.session.get('cart', {})
    subtotal = sum(float(i['price']) * i['quantity'] for i in cart.values())
    
    # Automatic Discount Logic
    discount = 0
    if subtotal > 1000:
        discount = 150
    elif subtotal > 500:
        discount = 50
        
    items_list = []
    for key, value in cart.items():
        item_data = value.copy()
        item_data['id'] = key
        item_data['total'] = value['price'] * value['quantity']
        items_list.append(item_data)

    return JsonResponse({
        'items': items_list,
        'subtotal': subtotal,
        'discount': discount,
        'total': subtotal - discount
    })

def update_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if item_id in cart:
            if action == 'inc':
                cart[item_id]['quantity'] += 1
            elif action == 'dec' and cart[item_id]['quantity'] > 1:
                cart[item_id]['quantity'] -= 1

            request.session['cart'] = cart
            request.session.modified = True

        return JsonResponse({'status': 'success'})

def remove_from_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        cart = request.session.get('cart', {})

        if item_id in cart:
            del cart[item_id]
            request.session['cart'] = cart
            request.session.modified = True

        return JsonResponse({'status': 'success'})

# --- Order Logic ---

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('Menu')
    
    if request.method == "POST":
        # Extract details from form
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Basic validation
        if not name or not phone or not address:
            # Re-render with error if fields are missing
            return render(request, 'checkout.html', {'error': 'Please fill all required delivery fields.'})

        # Payment specific validation
        if payment_method == 'card':
            card_number = request.POST.get('card_number')
            expiry = request.POST.get('expiry')
            cvv = request.POST.get('cvv')
            if not card_number or not expiry or not cvv:
                return render(request, 'checkout.html', {'error': 'Please provide all card details.'})
        elif payment_method == 'upi':
            upi_id = request.POST.get('upi_id')
            if not upi_id:
                return render(request, 'checkout.html', {'error': 'Please provide your UPI ID.'})

        subtotal = sum(float(i['price']) * i['quantity'] for i in cart.values())
        
        # Automatic Discount
        discount = 0
        if subtotal > 1000:
            discount = 150
        elif subtotal > 500:
            discount = 50
        
        total = subtotal - discount
        
        # Create the order with all details
        order = Order.objects.create(
            user=request.user, 
            name=name,
            phone=phone,
            email=email,
            address=address,
            payment_method=payment_method,
            total_amount=total
        )
        
        order_items_text = ""
        for item_id, d in cart.items():
            OrderItem.objects.create(
                order=order,
                item_name=d['name'],
                quantity=d['quantity'],
                price=d['price']
            )
            order_items_text += f"- {d['name']} (x{d['quantity']}): ₹{d['price'] * d['quantity']}\n"
        
        # Send Email for Successful Order
        if email:
            subject = f'Order Confirmed! Order #{order.id} - PDEU Bites'
            message = f'Hi {name},\n\nYour order has been placed successfully!\n\nOrder Summary:\n{order_items_text}\nTotal Amount: ₹{total}\nDelivery Address: {address}\n\nEstimated Delivery Time: 30-45 mins.\n\nThank you for choosing PDEU Bites!\n\nRegards,\nPDEU Bites Team'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        
        # Clear the cart
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('order_success', order_id=order.id)

    # Pre-fill user data if available
    context = {
        'pre_name': request.user.get_full_name() or request.user.username,
        'pre_email': request.user.email
    }
    # Reset abandonment email flag for this session attempt
    request.session['abandon_mail_sent'] = False
    return render(request, 'checkout.html', context)

from django.views.decorators.csrf import csrf_exempt

@login_required
def EditProfileView(request):
    """
    View for users to update their profile information.
    """
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('edit_profile')
        
    return render(request, 'edit_profile.html')

@csrf_exempt
def checkout_abandoned(request):
    """
    Called via JavaScript when a user leaves the checkout page without completing the order.
    """
    if request.user.is_authenticated and not request.session.get('abandon_mail_sent', False):
        email = request.user.email
        name = request.user.get_full_name() or request.user.username
        
        if email:
            try:
                subject = 'Did you forget something? - PDEU Bites'
                message = f'Hi {name},\n\nWe noticed you were checking out at PDEU Bites but didn\'t finish your order. Your delicious items are still in your cart!\n\nCome back and finish your order here: {"http://127.0.0.1:8000/checkout/"} \n\nRegards,\nPDEU Bites Team'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                request.session['abandon_mail_sent'] = True
            except Exception as e:
                print(f"Email error: {e}")
                
    return JsonResponse({'status': 'logged'})

def OrderHistoryView(request):
    """
    Displays the list of past orders for the logged-in user.
    Auto-updates status to 'Delivered' if > 30 mins old.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    from datetime import datetime, timezone, timedelta
    thirty_mins_ago = datetime.now(timezone.utc) - timedelta(minutes=30)
    
    # Auto-update status for this user's orders
    Order.objects.filter(
        user=request.user, 
        status__in=['Pending', 'Preparing'], 
        created_at__lt=thirty_mins_ago
    ).update(status='Delivered')
        
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def ManagerDashboardView(request):
    """
    Dashboard for restaurant staff to manage all orders.
    """
    if not request.user.is_staff:
        return redirect('Home')
        
    orders = Order.objects.all().order_by('-created_at')
    # Simple analytics
    total_revenue = sum(o.total_amount for o in orders if o.status == 'Delivered')
    pending_orders = orders.filter(status='Pending').count()
    
    return render(request, 'manager_dashboard.html', {
        'orders': orders,
        'total_revenue': total_revenue,
        'pending_count': pending_orders
    })

@login_required
def update_order_status(request, order_id):
    """
    AJAX view to update order status.
    """
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Preparing', 'Delivered']:
            order.status = new_status
            order.save()
            return JsonResponse({'status': 'success'})
            
    return JsonResponse({'status': 'error'}, status=400)

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=order)

    return render(request, 'order_success.html', {
        'order': order,
        'items': items
    })
