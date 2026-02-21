import getpass
from database_setup import initialize_system
from presentation_layer import presentation_class
from business_logic_layer import business_logic_class

def start_application():
    print("--- HAVE-WARE LOGIN ---")
    db_user = input("MySQL User: ") or "root"
    db_pass = getpass.getpass("MySQL Password: ")
    input("")
    
    config = {'host': 'localhost', 'user': db_user, 'password': db_pass}

    if initialize_system(config):
        logic = business_logic_class(config)
        app = presentation_class()
        app.store = logic
        app.main_menu()
    else:
        print("Login Failed.")

if __name__ == "__main__":
    start_application()