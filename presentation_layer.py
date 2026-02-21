import os, json
from business_logic_layer import business_logic_class

class presentation_class:
    def __init__(self):
        self.store = None
        self.custom_limits = json.load(open(os.path.join(os.path.dirname(__file__), "limits.json"))) if os.path.exists(os.path.join(os.path.dirname(__file__), "limits.json")) else {}
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        while True:
            self.clear_screen()
            print("========================================")
            print("   HAVE-WARE: ENTERPRISE MANAGEMENT")
            print("========================================")
            print("1. [Inventory] Add New Product")
            print("2. [Inventory] Update Price/Stock")
            print("3. [Inventory] Delete Product")
            print("4. [Billing]   Generate New GST Bill")
            print("5. [History]   View Sales Summary")
            print("6. [History]   Search Detailed Bill")
            print("7. [Alerts]    Set Custom Stock Limits")
            print("8. [Alerts]    View Smart Alerts")
            print("9. [Admin]     View Raw Database Tables")
            print("10.[AI]        AI Business Insights")
            print("0. Exit")
            choice = input("\nSelect Option: ")
            if choice == '1': self.manage_inventory()
            elif choice == '2': self.update_existing_item()
            elif choice == '3': self.remove_item_ui()
            elif choice == '4': self.new_bill()
            elif choice == '5': self.view_sales_history()
            elif choice == '6': self.view_detailed_bill()
            elif choice == '7': self.set_limit_ui()
            elif choice == '8': self.show_smart_alerts()
            elif choice == '9': self.view_custom_table()
            elif choice == '0': break
            elif choice == '10': self.show_ai_insights()

    def manage_inventory(self):
        self.clear_screen()
        print("--- INVENTORY MANAGEMENT ---")
        items = self.store.get_stock_report()
        print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Qty':<5}")
        for i in items:
            print(f"{i['item_id']:<5} {i['item_name']:<20} {i['price']:<10} {i['stock_qty']:<5}")
        try:
            iid = int(input("Item ID: "))
            name = input("Item Name: ")
            cat = input("Category: ")
            pr = float(input("Price: "))
            qt = int(input("Initial Stock: "))
            self.store.add_product(iid, name, cat, pr, qt)
            print("Product Added!")
        except ValueError: print("Invalid Input.")
        input("\nPress Enter...")

    def update_existing_item(self):
        self.clear_screen()
        try:
            iid = int(input("Enter Item ID: "))
            print("1. Update Price | 2. Update Stock")
            c = input("Choice: ")
            if c == '1':
                p = float(input("New Price: "))
                self.store.update_product_details(iid, price=p)
            elif c == '2':
                q = int(input("New Stock: "))
                self.store.update_product_details(iid, qty=q)
            print("Updated successfully.")
        except Exception as e: print(f"Error: {e}")
        input("\nPress Enter...")

    def remove_item_ui(self):
        self.clear_screen()
        try:
            iid = int(input("Enter Item ID to DELETE: "))
            if input(f"Confirm Delete #{iid}? (y/n): ").lower() == 'y':
                if self.store.delete_product(iid):
                    print("Deleted.")
        except ValueError: print("Invalid ID.")
        input("\nPress Enter...")

    def new_bill(self):
        self.clear_screen()
        customer = input("Customer Name: ")
        cart = []
        while True:
            try:
                iid = int(input("Enter Item ID (0 to finish): "))
                if iid == 0: break
                qty = int(input("Quantity: "))
                if self.store.validate_stock(iid, qty):
                    item = [i for i in self.store.get_stock_report() if i['item_id'] == iid][0]
                    cart.append({'id': iid, 'name': item['item_name'], 'price': float(item['price']), 'qty': qty, 'line_total': float(item['price']) * qty})
                    print(f"Added {item['item_name']}")
                else: print("Insufficient stock!")
            except Exception:
                print("Invalid Input")
                break
        if cart:
            res = self.store.finalize_sale(customer, cart)
            if res: print(f"Bill Generated! Total: {res[2]}")
        input("\nPress Enter...")

    def view_sales_history(self):
        self.clear_screen()
        data = self.store.get_sales_history()
        for r in data: print(f"ID: {r['bill_id']} | {r['customer_name']} | Total: {r['grand_total']}")
        input("\nPress Enter...")

    def view_detailed_bill(self):
        try:
            self.clear_screen()
            bid = int(input("Enter Bill ID: "))
            items = self.store.get_bill_details(bid)
            for i in items: print(f"{i['item_name']} x {i['qty_sold']} = {i['line_total']}")
            input("\nPress Enter...")
        except Exception:
            print("Invalid Input")
            input("\nPress Enter...")

    def set_limit_ui(self):
        try:
            self.clear_screen()
            iid = int(input("Item ID: "))
            lim = int(input("Limit: "))
            self.custom_limits[str(iid)] = lim
            print("Limit Set.")
            json.dump(self.custom_limits, open(os.path.join(os.path.dirname(__file__), "limits.json"), "w"))
            input("\nPress Enter...")
        except Exception:
            print("Invalid Input")
            input("\nPress Enter...")

    def show_smart_alerts(self):
        self.clear_screen()
        alerts = self.store.get_custom_low_stock_alerts(self.custom_limits)
        for a in alerts: print(f"ALERT: {a['item_name']} (Stock: {a['stock_qty']}, Limit: {a['current_limit']})")
        input("\nPress Enter...")

    def view_custom_table(self):
        try:
            self.clear_screen()
            opt = input("Table \n1 for inventory \n2 for sales_header \n3 for sales_items):\nChoice : ")
            opt1 = {"1":"inventory","2":"sales_header","3":"sales_items"}
            data = self.store.get_any_table(opt1[opt])
            if data:
                for row in data: print(row)
            input("\nPress Enter...")
        except Exception:
            print("Invalid Input")
            input("\nPress Enter...")

    def show_ai_insights(self):
        self.clear_screen()
    
        from business_logic_layer import BusinessAI
        ai = BusinessAI(self.store.db)
        raw_data = ai.get_deep_insights()
        smart_advice = ai.generate_smart_advice(raw_data)

        print("\n" + "="*50)
        print("          Have-Ware Intelligence Report ")
        print("="*50)

        # Performance Score
        rev = raw_data['metrics'][0]['rev'] or 0
        count = raw_data['metrics'][0]['count'] or 0
        avg_bill = round(rev/count, 2) if count > 0 else 0
        
        print(f" Business Health Code: {'Good' if avg_bill > 500  else 'Unstable'}")
        print(f" Average Sale: ₹{avg_bill}")
        print("-" * 50)

        print(" Ai Analysis:")
        if not smart_advice:
            print("   > AI needs more transaction history to identify patterns.")
        else:
            for line in smart_advice:
                print(f"   {line}")

        print("\n" + "="*50)
        input("Press Enter to close AI Dashboard...")