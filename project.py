import sqlite3

# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('simple_crm.db')
cursor = conn.cursor()

# Create table for customers
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
)
''')

# Create table for customer interactions
cursor.execute('''
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    interaction_date TEXT,
    interaction_type TEXT,
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
''')

# Function to add a new customer
def add_customer(first_name, last_name, email, phone):
    cursor.execute('''
    INSERT INTO customers (first_name, last_name, email, phone)
    VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, email, phone))
    conn.commit()
    print(f'Customer {first_name} {last_name} added successfully.')

# Function to view all customers
def view_customers():
    cursor.execute('SELECT * FROM customers')
    customers = cursor.fetchall()
    if customers:
        for customer in customers:
            print(f'ID: {customer[0]}, Name: {customer[1]} {customer[2]}, Email: {customer[3]}, Phone: {customer[4]}')
    else:
        print("No customers found.")

# Function to update a customer's information
def update_customer(customer_id, first_name=None, last_name=None, email=None, phone=None):
    query = 'UPDATE customers SET '
    params = []
    
    if first_name:
        query += 'first_name = ?, '
        params.append(first_name)
    if last_name:
        query += 'last_name = ?, '
        params.append(last_name)
    if email:
        query += 'email = ?, '
        params.append(email)
    if phone:
        query += 'phone = ?, '
        params.append(phone)
    
    query = query.rstrip(', ')  # Remove last comma
    query += ' WHERE id = ?'
    params.append(customer_id)
    
    cursor.execute(query, tuple(params))
    conn.commit()
    print(f'Customer {customer_id} updated successfully.')

# Function to track interactions with customers
def add_interaction(customer_id, interaction_date, interaction_type, notes):
    cursor.execute('''
    INSERT INTO interactions (customer_id, interaction_date, interaction_type, notes)
    VALUES (?, ?, ?, ?)
    ''', (customer_id, interaction_date, interaction_type, notes))
    conn.commit()
    print(f'Interaction added for customer {customer_id}.')

# Function to view customer interactions
def view_interactions(customer_id):
    cursor.execute('''
    SELECT * FROM interactions WHERE customer_id = ?
    ''', (customer_id,))
    interactions = cursor.fetchall()
    if interactions:
        for interaction in interactions:
            print(f'ID: {interaction[0]}, Date: {interaction[2]}, Type: {interaction[3]}, Notes: {interaction[4]}')
    else:
        print(f'No interactions found for customer {customer_id}.')

# Example usage of CRM functions
if _name_ == "_main_":
    while True:
        print("\nCRM System Menu:")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Update Customer")
        print("4. Add Interaction")
        print("5. View Interactions")
        print("6. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            add_customer(first_name, last_name, email, phone)

        elif choice == '2':
            view_customers()

        elif choice == '3':
            customer_id = int(input("Enter customer ID to update: "))
            first_name = input("Enter new first name (or press Enter to skip): ")
            last_name = input("Enter new last name (or press Enter to skip): ")
            email = input("Enter new email (or press Enter to skip): ")
            phone = input("Enter new phone (or press Enter to skip): ")
            update_customer(customer_id, first_name, last_name, email, phone)

        elif choice == '4':
            customer_id = int(input("Enter customer ID for interaction: "))
            interaction_date = input("Enter interaction date (YYYY-MM-DD): ")
            interaction_type = input("Enter interaction type (call, email, etc.): ")
            notes = input("Enter notes about the interaction: ")
            add_interaction(customer_id, interaction_date, interaction_type, notes)

        elif choice == '5':
            customer_id = int(input("Enter customer ID to view interactions: "))
            view_interactions(customer_id)

        elif choice == '6':
            print("Exiting CRM System.")
            break

        else:
            print("Invalid choice. Please try again.")

# Close the connection when done
conn.close()
