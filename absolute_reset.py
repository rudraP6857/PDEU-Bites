import os
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Resturant_Project.settings')
django.setup()

from Base_App.models import Order, OrderItem

def absolute_reset():
    # 1. Clear all order data from Django
    print(f"Deleting {Order.objects.count()} orders...")
    Order.objects.all().delete()
    OrderItem.objects.all().delete()
    
    # 2. Directly reach into SQLite and wipe the sequence
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if they exist first
    cursor.execute("SELECT * FROM sqlite_sequence WHERE name IN ('Base_App_order', 'Base_App_orderitem')")
    print("Sequences before reset:", cursor.fetchall())
    
    # Reset them
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'Base_App_order'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'Base_App_orderitem'")
    
    # Optional: also try updating to 0 if delete didn't work for some reason
    cursor.execute("INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('Base_App_order', 0)")
    cursor.execute("INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('Base_App_orderitem', 0)")
    
    conn.commit()
    
    cursor.execute("SELECT * FROM sqlite_sequence WHERE name IN ('Base_App_order', 'Base_App_orderitem')")
    print("Sequences after reset:", cursor.fetchall())
    
    conn.close()
    print("Order data cleared and counter reset to 0.")

if __name__ == '__main__':
    absolute_reset()
