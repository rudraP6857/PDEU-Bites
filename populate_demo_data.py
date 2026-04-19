import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Resturant_Project.settings')
django.setup()

from Base_App.models import Items, ItemList, Feedback

def populate():
    # 1. Add New Items
    burger_cat, _ = ItemList.objects.get_or_create(Category_name='Burger')
    pizza_cat, _ = ItemList.objects.get_or_create(Category_name='Pizza')
    pasta_cat, _ = ItemList.objects.get_or_create(Category_name='Pasta')
    
    new_items = [
        {'name': 'Spicy Paneer Burger', 'desc': 'Crispy paneer with tandoori mayo.', 'price': 180, 'cat': burger_cat},
        {'name': 'Veggie Overload Pizza', 'desc': 'Loaded with olives, corn, and peppers.', 'price': 350, 'cat': pizza_cat},
        {'name': 'White Sauce Pasta', 'desc': 'Creamy alfredo with mushrooms.', 'price': 220, 'cat': pasta_cat},
        {'name': 'Chocolate Lava Cake', 'desc': 'Molten chocolate center.', 'price': 120, 'cat': pizza_cat},
    ]
    
    for item in new_items:
        Items.objects.get_or_create(
            Item_name=item['name'],
            defaults={'description': item['desc'], 'Price': item['price'], 'Category': item['cat']}
        )
    
    # 2. Add Feedbacks (Indian Young People)
    feedbacks = [
        {'name': 'Rohan Sharma', 'email': 'rohan@gmail.com', 'msg': 'Best burgers in Gandhinagar! The tandoori mayo is just 🔥. Perfect place for a weekend treat.', 'rating': 5},
        {'name': 'Ananya Iyer', 'email': 'ananya.i@outlook.com', 'msg': 'Ordered the overload pizza. The crust was so fresh. Love the vibe of PDEU Bites!', 'rating': 5},
        {'name': 'Ishaan Patel', 'email': 'ishaan22@gmail.com', 'msg': 'Great service. The delivery was exactly on time. Value for money for students like us.', 'rating': 4},
        {'name': 'Meera Deshmukh', 'email': 'meera_d@yahoo.com', 'msg': 'White sauce pasta is a must try! Very creamy and authentic. Highly recommended.', 'rating': 5},
        {'name': 'Siddharth Varma', 'email': 'sidv@gmail.com', 'msg': 'The discount system is cool. Got ₹150 off on our group order. Cheers!', 'rating': 5}
    ]
    
    for f in feedbacks:
        Feedback.objects.get_or_create(
            User_name=f['name'],
            Email=f['email'],
            defaults={'Description': f['msg'], 'Rating': f['rating']}
        )
    
    print("Demo data populated successfully!")

if __name__ == '__main__':
    populate()
