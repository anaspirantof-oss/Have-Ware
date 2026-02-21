import mysql.connector as msql

def initialize_system(db_config):
    try:
        connection = msql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS haveware_db")
        cursor.execute("USE haveware_db")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
            item_id INT PRIMARY KEY,
            item_name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10, 2),
            stock_qty INT)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS sales_header (
            bill_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_name VARCHAR(100),
            bill_date DATE,
            sub_total DECIMAL(10, 2),
            gst_amount DECIMAL(10, 2),
            grand_total DECIMAL(10, 2))""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS sales_items (
            id INT PRIMARY KEY AUTO_INCREMENT,
            bill_id INT,
            item_id INT,
            qty_sold INT,
            unit_price DECIMAL(10, 2),
            line_total DECIMAL(10, 2),
            FOREIGN KEY (bill_id) REFERENCES sales_header(bill_id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES inventory(item_id) ON DELETE CASCADE)""")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except msql.Error as err:
        print(f"Setup Failed: {err}")
        return False