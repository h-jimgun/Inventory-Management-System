import requests

API_URL = "http://127.0.0.1:5000/product"

def show_menu():
    print("\n ---Inventory CLI---")
    print("1, View all items")
    print("2. Add a new item by Barcode (Open Food Facts Api)")
    print("3. Update an item's name")
    print("4. Delete an item")
    print ("5. Exit")
    return input ("Choose an option: ")

def view_all():
    response = requests.get(API_URL)
    if response.status_code == 200:
        products = response.json()

        if not products:
            print("Inventory is empty.")
        for p in products:
            print(f"[{p['id']}] {p['name']} (Brand: {p['brands']}) - Barcode : {p['barcode']}")
    else:
         print ("Failed to load inventory. Status code: {response.status_code}")

def add_item():
    barcode = input("Enter the product barcode: ")
       
    response = requests.post(API_URL, json={"barcode": barcode})
    
    if response.status_code == 201:
        data = response.json()
        print(f"Success! Added: {data['name']} by {data['brands']}")
    else:       
        print(f"Error: {response.json().get('Error')}")

def update_item():
    item_id = input("Enter item ID to update: ")
    new_name = input("Enter the new name: ")
    
    response = requests.patch(f"{API_URL}/{item_id}", json={"name": new_name})
    
    if response.status_code == 200:
        print("Update successful!")
    else:
        print("Error: Item not found or bad request.")

def delete_item():
    item_id = input("Enter item ID to delete: ")
    response = requests.delete(f"{API_URL}/{item_id}")
    
    if response.status_code == 204:
        print("Item deleted.")
    else:
        print("Error: Item not found.")

if __name__ == "__main__":
    while True:
        choice = show_menu()
        if choice == "1":
            view_all()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

