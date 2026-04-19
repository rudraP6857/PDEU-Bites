import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Resturant_Project.settings')
django.setup()

from Base_App.models import Items

def update_burger():
    item = Items.objects.filter(Item_name='Spicy Paneer Burger').first()
    if item:
        item.Image = 'items/paneer_burger.png'
        item.save()
        print('Spicy Paneer Burger image updated successfully!')
    else:
        print('Spicy Paneer Burger item not found.')

if __name__ == '__main__':
    update_burger()
