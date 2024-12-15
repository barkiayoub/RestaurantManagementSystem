import sqlite3

# Reservations table
def reservations_table():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    
    # Sample reservations
    reservations = [
        ("Ayoub", "0612345678", 5, "2024-12-15", "19:00"),
        ("Fatima", "0623456789", 3, "2024-12-16", "20:30"),
        ("Ahmed", "0634567890", 1, "2024-12-17", "12:00"),
        ("Khadija", "0645678901", 4, "2024-12-18", "21:00"),
        ("Mohammed", "0656789012", 2, "2024-12-19", "18:00"),
    ]
    
    cursor.executemany('''
        INSERT INTO reservations (name, phone, table_number, date, time)
        VALUES (?, ?, ?, ?, ?)
    ''', reservations)
    
    conn.commit()
    conn.close()


# Foods table
def foods_table():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    
    # Moroccan foods
    moroccan_foods = [
        ("Tagine", "A slow-cooked meat, vegetables, and spices, cooked in a traditional clay pot.", 80.00),
        ("Couscous", "Steamed semolina served with vegetables, meat, and a savory broth.", 70.00),
        ("Pastilla", "A sweet and savory pie made with thin pastry, chicken, almonds, and spices.", 90.00),
        ("Harira", "A traditional soup made with tomatoes, lentils, chickpeas, and lamb.", 40.00),
        ("Rfissa", "Chicken served with lentils and fenugreek over a bed of shredded bread.", 85.00),
        ("Mechoui", "Slow-roasted lamb seasoned with Moroccan spices.", 120.00),
        ("Briouat", "Fried pastries stuffed with minced meat, cheese, or almonds.", 30.00),
        ("Zaalouk", "A cooked salad made with eggplant, tomatoes, garlic, and spices.", 25.00),
        ("Kefta Tagine", "Meatballs cooked in a spicy tomato sauce, often topped with eggs.", 75.00),
        ("Mint Tea", "Traditional Moroccan tea made with green tea, fresh mint, and sugar.", 20.00),
    ]
    
    cursor.executemany('''
        INSERT INTO foods (name, description, price)
        VALUES (?, ?, ?)
    ''', moroccan_foods)
    
    conn.commit()
    conn.close()


# Orders table
def orders_table():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    
    # Sample orders
    sample_orders = [
        ("Ayoub", 5, "Tagine", 2, 160.00),
        ("Fatima", 3, "Couscous", 3, 210.00),
        ("Ahmed", 1, "Harira", 1, 40.00),
        ("Khadija", 4, "Pastilla", 2, 180.00),
        ("Mohammed", 2, "Mechoui", 1, 120.00),
    ]
    
    cursor.executemany('''
        INSERT INTO orders (customer_name, table_number, food_name, quantity, total_price)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_orders)
    
    conn.commit()
    conn.close()


# Initialize database and populate tables
reservations_table()
foods_table()
orders_table()
