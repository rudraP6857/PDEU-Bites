import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Resturant_Project.settings')
django.setup()

from Base_App.models import Order

def update_order():
    order = Order.objects.filter(id=1).first()
    if order:
        order.status = 'Delivered'
        order.save()
        print(f"Order #{order.id} status updated to Delivered successfully!")
    else:
        print("Order #1 not found.")

if __name__ == '__main__':
    update_order()
