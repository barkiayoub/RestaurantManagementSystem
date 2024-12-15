import sqlite3
import db_setup
from customtkinter import CTk, CTkComboBox, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkOptionMenu, CTkScrollableFrame, CTkTabview

# Functions for database operations

def save_reservation(name, phone, table_number, date, time):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reservations (name, phone, table_number, date, time)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, phone, table_number, date, time))
    conn.commit()
    conn.close()

def fetch_reservations():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_reservation(reservation_id):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
    conn.commit()
    conn.close()

def save_food(name, description, price):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO foods (name, description, price)
        VALUES (?, ?, ?)
    ''', (name, description, price))
    conn.commit()
    conn.close()

def fetch_foods():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM foods")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_foods_list(): # For the dropdown list
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM foods")
    food_list = [row[0] for row in cursor.fetchall()]  # Extract food names into a list
    conn.close()
    return food_list

def update_food(food_id, name, description, price):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE foods
        SET name = ?, description = ?, price = ?
        WHERE id = ?
    ''', (name, description, price, food_id))
    conn.commit()
    conn.close()

def delete_food(food_id):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM foods WHERE id = ?", (food_id,))
    conn.commit()
    conn.close()

def save_order(customer_name, table_number, food_name, quantity, total_price):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (customer_name, table_number, food_name, quantity, total_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_name, table_number, food_name, quantity, total_price))
    conn.commit()
    conn.close()

def fetch_orders():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_orders(order_id):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE table_number = ?", (order_id,))
    order = cursor.fetchone()
    return order
        
     

def delete_order(order_table_number):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE table_number = ?", (order_table_number,))
    conn.commit()
    conn.close()

def fetch_orders_by_customer():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT customer_name, sum(total_price)*quantity AS price, GROUP_CONCAT(food_name || ' x' || quantity || ' (MAD' || total_price || ')', '; ') AS details
        FROM orders
        GROUP BY customer_name
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_orders_by_table_number():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT table_number, sum(total_price)*quantity AS price, GROUP_CONCAT(food_name || ' x' || quantity || ' (MAD' || total_price || ')', '; ') AS details
        FROM orders
        GROUP BY table_number
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


# Application GUI class
class RestaurantApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("Restaurant Management")
        self.geometry("800x600")

        self.initialize_ui()

    def initialize_ui(self):
        # Tabview for navigation
        self.tabview = CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        # Reservations tab
        self.reservation_tab = self.tabview.add("Reservations")
        self.initialize_reservations_ui(self.reservation_tab)

        # Foods tab
        self.food_tab = self.tabview.add("Foods")
        self.initialize_food_ui(self.food_tab)

        # Orders tab
        self.order_tab = self.tabview.add("Orders")
        self.initialize_order_ui(self.order_tab)

        # Order Details tab
        self.order_details_tab = self.tabview.add("Order Details")
        self.initialize_order_details_ui(self.order_details_tab)

    def initialize_reservations_ui(self, tab):
        # Header
        header_label = CTkLabel(tab, text="Restaurant Reservations", font=("Arial", 20))
        header_label.pack(pady=20)

        # Input frame
        input_frame = CTkFrame(tab)
        input_frame.pack(pady=10, padx=20, fill="x")

        name_label = CTkLabel(input_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = CTkEntry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        phone_label = CTkLabel(input_frame, text="Phone:")
        phone_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = CTkEntry(input_frame)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        table_label = CTkLabel(input_frame, text="Table Number:")
        table_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.table_entry = CTkEntry(input_frame)
        self.table_entry.grid(row=2, column=1, padx=10, pady=5)

        date_label = CTkLabel(input_frame, text="Date (YYYY-MM-DD):")
        date_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = CTkEntry(input_frame)
        self.date_entry.grid(row=3, column=1, padx=10, pady=5)

        time_label = CTkLabel(input_frame, text="Time (HH:MM):")
        time_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.time_entry = CTkEntry(input_frame)
        self.time_entry.grid(row=4, column=1, padx=10, pady=5)

        save_button = CTkButton(input_frame, text="Save Reservation", command=self.save_reservation)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Reservations display frame
        self.reservations_display_frame = CTkScrollableFrame(tab)
        self.reservations_display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        

        self.load_reservations()

    def initialize_food_ui(self, tab):
        # Header
        header_label = CTkLabel(tab, text="Available Foods", font=("Arial", 20))
        header_label.pack(pady=20)

        # Input frame
        input_frame = CTkFrame(tab)
        input_frame.pack(pady=10, padx=20, fill="x")

        food_name_label = CTkLabel(input_frame, text="Name:")
        food_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.food_name_entry = CTkEntry(input_frame)
        self.food_name_entry.grid(row=0, column=1, padx=10, pady=5)

        description_label = CTkLabel(input_frame, text="Description:")
        description_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.food_description_entry = CTkEntry(input_frame)
        self.food_description_entry.grid(row=1, column=1, padx=10, pady=5)

        price_label = CTkLabel(input_frame, text="Price:")
        price_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.food_price_entry = CTkEntry(input_frame)
        self.food_price_entry.grid(row=2, column=1, padx=10, pady=5)

        save_button = CTkButton(input_frame, text="Add Food", command=self.add_food)
        save_button.grid(row=3, column=0, pady=5)

        # Foods display frame
        self.foods_display_frame = CTkScrollableFrame(tab)
        self.foods_display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.load_foods()

    def initialize_order_ui(self, tab):
        # Header
        header_label = CTkLabel(tab, text="Orders", font=("Arial", 20))
        header_label.pack(pady=20)

        # Input frame
        input_frame = CTkFrame(tab)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        # Customer Name Input
        customer_name_label = CTkLabel(input_frame, text="Customer Name:")
        customer_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.customer_name_entry = CTkEntry(input_frame)
        self.customer_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Table Number Input
        table_number_label = CTkLabel(input_frame, text="Table Number:")
        table_number_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.table_number_entry = CTkEntry(input_frame)
        self.table_number_entry.grid(row=1, column=1, padx=10, pady=5)

        # Food Name Input
        food_name_label = CTkLabel(input_frame, text="Food Name:")
        food_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            # Create a dropdown menu with fetched food items
        self.order_food_name_dropdown = CTkOptionMenu(input_frame, values=fetch_foods_list())
        self.order_food_name_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Quantity Input
        quantity_label = CTkLabel(input_frame, text="Quantity:")
        quantity_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.order_quantity_entry = CTkEntry(input_frame)
        self.order_quantity_entry.grid(row=3, column=1, padx=10, pady=5)

        # Total Price Input
        total_price_label = CTkLabel(input_frame, text="Total Price:")
        total_price_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.order_total_price_entry = CTkEntry(input_frame)
        self.order_total_price_entry.grid(row=4, column=1, padx=10, pady=5)

        # Add Order Button
        save_button = CTkButton(input_frame, text="Add Order", command=self.add_order)
        save_button.grid(row=5, column=0, pady=5)

        # Search Orders by table
        search_frame = CTkFrame(tab)
        search_frame.pack(pady=10, padx=20, fill="x")

        search_label = CTkLabel(search_frame, text="Search by Table Number:")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.search_entry = CTkEntry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        order_id = self.search_entry.get()

        search_button = CTkButton(search_frame, text="Search", command=search_orders(order_id))
        search_button.grid(row=0, column=2, padx=10, pady=5)

        # print(search_orders(order_id))

        # Orders display frame
        self.orders_display_frame = CTkScrollableFrame(tab)
        self.orders_display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Load existing orders
        self.load_orders()

    


    def initialize_order_details_ui(self, tab):
        # Header
        header_label = CTkLabel(tab, text="Order Details by Customer", font=("Arial", 20))
        header_label.pack(pady=20)

        #Refresh Order details
        refresh_button = CTkButton(header_label, text="Refresh Orders List", command=self.load_order_details)
        refresh_button.grid(row=4, column=0, pady=5)

        # Display frame
        self.order_details_display_frame = CTkScrollableFrame(tab)
        self.order_details_display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.load_order_details()




    def load_order_details(self):
        # Clear previous content
        for widget in self.order_details_display_frame.winfo_children():
            widget.destroy()

        # Fetch orders grouped by customer
        orders = fetch_orders_by_customer()

        for customer, price, details in orders:
            customer_label = CTkLabel(self.order_details_display_frame, text=f"Customer: {customer}", font=("Arial", 16))
            customer_label.pack(anchor="w", padx=10, pady=5)

            details_label = CTkLabel(self.order_details_display_frame, text=f"Orders: {details} Totale price: {price}", wraplength=700)
            details_label.pack(anchor="w", padx=20, pady=5)


    def save_reservation(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        table_number = self.table_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        if name and phone and table_number and date and time:
            save_reservation(name, phone, int(table_number), date, time)
            self.clear_reservation_inputs()
            self.load_reservations()
        else:
            self.show_error("Please fill all fields!")

    def load_reservations(self):
        for widget in self.reservations_display_frame.winfo_children():
            widget.destroy()

        reservations = fetch_reservations()
        for reservation in reservations:
            reservations_frame = CTkFrame(self.reservations_display_frame)
            reservations_frame.pack(fill="x", padx=10, pady=5)    

            label = CTkLabel(reservations_frame, text=f"{reservation[1]} | {reservation[2]} | Table {reservation[3]} | {reservation[4]} {reservation[5]}", anchor="w")
            label.pack(side='left',fill="x", expand=True)

            delete_button = CTkButton(reservations_frame, text="Clear table", command=lambda oid=reservation[0]: self.delete_reservation(oid))
            delete_button.pack(side="right")

    def delete_reservation(self, reservation_id):
        delete_reservation(reservation_id)
        self.load_reservations()

    def clear_reservation_inputs(self):
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.table_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.time_entry.delete(0, 'end')

    def add_food(self):
        name = self.food_name_entry.get()
        description = self.food_description_entry.get()
        price = self.food_price_entry.get()

        if name and description and price:
            save_food(name, description, float(price))
            self.clear_food_inputs()
            self.load_foods()
        else:
            self.show_error("Please fill all fields!")

    def load_foods(self):
        for widget in self.foods_display_frame.winfo_children():
            widget.destroy()

        foods = fetch_foods()
        for food in foods:
            food_frame = CTkFrame(self.foods_display_frame)
            food_frame.pack(fill="x", padx=10, pady=5)

            food_label = CTkLabel(food_frame, text=f"{food[1]} | {food[2]} | MAD{food[3]:.2f}", anchor="w")
            food_label.pack(side="left", fill="x", expand=True)

            delete_button = CTkButton(food_frame, text="Delete", command=lambda fid=food[0]: self.delete_food(fid))
            delete_button.pack(side="right")

    def delete_food(self, food_id):
        delete_food(food_id)
        self.load_foods()

    def clear_food_inputs(self):
        self.food_name_entry.delete(0, 'end')
        self.food_description_entry.delete(0, 'end')
        self.food_price_entry.delete(0, 'end')

    def add_order(self):
        customer_name = self.customer_name_entry.get()
        table_number = self.table_number_entry.get()
        food_name = self.order_food_name_entry.get()
        quantity = self.order_quantity_entry.get()
        total_price = self.order_total_price_entry.get()

        if customer_name and food_name and quantity and total_price:
            save_order(customer_name, table_number, food_name, int(quantity), float(total_price))
            self.clear_order_inputs()
            self.load_orders()
        else:
            self.show_error("Please fill all fields!")

    def load_orders(self):
        for widget in self.orders_display_frame.winfo_children():
            widget.destroy()

        orders = fetch_orders_by_table_number()

        for table_number,price, details in orders:
            orders_display_frame = CTkLabel(self.orders_display_frame, text=f"Table: {table_number}", font=("Arial", 16))
            orders_display_frame.pack(anchor="w", padx=10, pady=5)

            details_label = CTkLabel(self.orders_display_frame, text=f"Orders: {details} Totale price: {price}", wraplength=700)
            details_label.pack(anchor="w", padx=20, pady=5)
            
    def delete_order(self, order_id):
        delete_order(order_id)
        self.load_orders()

    def clear_order_inputs(self):
        self.order_food_name_entry.delete(0,'end')
        self.order_quantity_entry.delete(0,'end')
        self.order_total_price_entry.delete(0,'end')

if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()