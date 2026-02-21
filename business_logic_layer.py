from data_layer import data_class
from datetime import date

class business_logic_class:
    def __init__(self, db_config):
        self.db = data_class(db_config)

    def calculate_gst(self, amount, rate=18):
        tax = amount * (rate / 100)
        return round(tax, 2)

    def add_product(self, item_id, name, cat, price, qty):
        query = "INSERT INTO inventory (item_id, item_name, category, price, stock_qty) VALUES (%s, %s, %s, %s, %s)"
        return self.db.execute_write(query, (item_id, name, cat, price, qty))

    def update_product_details(self, item_id, price=None, qty=None):
        if price is not None:
            query = "UPDATE inventory SET price = %s WHERE item_id = %s"
            return self.db.execute_write(query, (price, item_id))
        if qty is not None:
            query = "UPDATE inventory SET stock_qty = %s WHERE item_id = %s"
            return self.db.execute_write(query, (qty, item_id))

    def delete_product(self, item_id):
        query = "DELETE FROM inventory WHERE item_id = %s"
        return self.db.execute_write(query, (item_id,))

    def get_stock_report(self):
        return self.db.execute_read("SELECT * FROM inventory")

    def get_custom_low_stock_alerts(self, threshold_map):
        all_stock = self.get_stock_report()
        alerts = []
        for item in all_stock:
            limit = threshold_map.get(str(item['item_id']), 5) # Default 5
            if item['stock_qty'] <= limit:
                item['current_limit'] = limit
                alerts.append(item)
        return alerts

    def get_sales_history(self):
        return self.db.execute_read("SELECT * FROM sales_header ORDER BY bill_id DESC")

    def get_bill_details(self, bill_id):
        query = """SELECT si.item_id, i.item_name, si.qty_sold, si.unit_price, si.line_total 
                   FROM sales_items si JOIN inventory i ON si.item_id = i.item_id
                   WHERE si.bill_id = %s"""
        return self.db.execute_read(query, (bill_id,))

    def validate_stock(self, item_id, requested_qty):
        query = "SELECT stock_qty FROM inventory WHERE item_id = %s"
        result = self.db.execute_read(query, (item_id,))
        return result and result[0]['stock_qty'] >= requested_qty

    def finalize_sale(self, customer_name, cart):
        sub_total = sum(item['line_total'] for item in cart)
        gst = self.calculate_gst(sub_total)
        grand_total = sub_total + gst
        header_sql = "INSERT INTO sales_header (customer_name, bill_date, sub_total, gst_amount, grand_total) VALUES (%s, %s, %s, %s, %s)"
        bill_id = self.db.execute_write(header_sql, (customer_name, date.today(), sub_total, gst, grand_total))
        if bill_id:
            for item in cart:
                self.db.execute_write("INSERT INTO sales_items (bill_id, item_id, qty_sold, unit_price, line_total) VALUES (%s, %s, %s, %s, %s)", (bill_id, item['id'], item['qty'], item['price'], item['line_total']))
                self.db.execute_write("UPDATE inventory SET stock_qty = stock_qty - %s WHERE item_id = %s", (item['qty'], item['id']))
            return bill_id, gst, grand_total
        return None

    def get_any_table(self, table_name):
        if table_name in ["inventory", "sales_header", "sales_items"]:
            return self.db.execute_read(f"SELECT * FROM {table_name}")
        return None

class BusinessAI:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_deep_insights(self):
        #Perform heuristic analysis on sales patterns
        results = {}

        # Logic: Find items frequently appearing in the same bill_id
        assoc_query = """
            SELECT a.item_id as item1, b.item_id as item2, COUNT(*) as frequency
            FROM sales_items a 
            JOIN sales_items b ON a.bill_id = b.bill_id AND a.item_id < b.item_id
            GROUP BY item1, item2 ORDER BY frequency DESC LIMIT 1
        """
        results['associations'] = self.db.execute_read(assoc_query)

        # Logic: Compare stock levels with how much has been sold
        health_query = """
            SELECT i.item_name, i.stock_qty, IFNULL(SUM(si.qty_sold), 0) as sold_total
            FROM inventory i
            LEFT JOIN sales_items si ON i.item_id = si.item_id
            GROUP BY i.item_id
        """
        results['health'] = self.db.execute_read(health_query)

        # Logic: High volume vs. High margin
        results['metrics'] = self.db.execute_read("SELECT SUM(grand_total) as rev, COUNT(bill_id) as count FROM sales_header")
        
        return results

    def generate_smart_advice(self, data):
        # Generates human-like advice based on data points.
        advice = []
        
        # Analyze Association
        if data['associations']:
            pair = data['associations'][0]
            advice.append(f" PATTERN DETECTED: Customers often buy Item #{pair['item1']} and Item #{pair['item2']} together.")
            advice.append(f" STRATEGY: Create a 'Bundle Discount' for these items to increase ticket size.")

        # Analyze Health
        for item in data['health']:
            if item['sold_total'] > 20 and item['stock_qty'] < 10:
                advice.append(f" VELOCITY ALERT: '{item['item_name']}' is selling fast but stock is critical.")
            elif item['sold_total'] == 0 and item['stock_qty'] > 50:
                advice.append(f" DEAD STOCK: '{item['item_name']}' has zero sales. Consider a clearance sale.")

        return advice