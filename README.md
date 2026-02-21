# Have-Ware Enterprise Management System

This Project is completely open-source and every possible improvement is welcomed at the fullest.

Have-Ware is a robust, CUI-based Inventory and Billing Management System built with Python and MySQL. 

This project demonstrates a clean **3-tier architecture** (Presentation, Business Logic, and Data layers) and features an AI-inspired business insights module to track sales velocity and product associations.

## 🚀 Features
* **Modular Architecture:** Clean separation of UI, logic, and database operations.
* **Automated Database Setup:** Automatically initializes the `haveware_db` database and required tables upon first run.
* **Inventory Management:** Add, update, delete, and monitor stock levels.
* **Billing & Sales:** Generate GST-inclusive bill amount, validate stock in real-time, and view detailed sales history.
* **Smart Alerts:** Set custom low-stock thresholds for individual items.
* **AI Business Insights:** Heuristic analysis to detect product associations (items bought together) and sales velocity.

## 🛠️ Tech Stack
* **Language:** Python 3.15.0a1
* **Database:** MySQL 8.0
* **Libraries:** `mysql-connector-python`

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/anaspirantof-oss/Have-Ware.git](https://github.com/anaspirantof-oss/Have-Ware.git)
   cd haveware-inventory-management
   
2. **Install dependencies:**
   
   Ensure MySQL is running:
   Make sure your local MySQL server is active. The program will automatically create the required database and schema for you.
   ```bash
   pip install -r requirements.txt

4. **Run the application:**

   ```bash
   python main.py
   
## 🔒 Security Note
This application does not hardcode any database credentials. Upon running main.py, you will be securely prompted to enter your MySQL username and password via the terminal.

## 📂 Project Structure
1. ```main.py```
   Application entry point and secure login.

2. ```presentation_layer.py```
   Command-line interface and user menus.

3. ```business_logic_layer.py```
   Core logic, GST calculations, AI insights.

4. ```data_layer.py```
   Secure MySQL database connection and CRUD operations.

5. ```database_setup.py```
   Automated schema initialization.

6. ```limits.json```
   Local storage for custom inventory alert thresholds.

## End
This Project was developed during the making of my class 12th cbse computer science IRP 2026-27 and was my first steps into programming. Any Bugs and Mistakes found are completely understable and every possible way is tried to keep it updated from bugs.

## Thank You
