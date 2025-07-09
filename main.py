import json
import datetime
import os
from collections import defaultdict

class ChargingPointSystem:
    def _init_(self):
        self.DATA_DIR = "data"
        os.makedirs(self.DATA_DIR, exist_ok=True)
        
        # Define device types and prices
        self.DEVICE_TYPES = {
            '1': {'name': 'Mobile', 'with_charger': 5, 'without_charger': 7},
            '2': {'name': 'Small Battery', 'with_charger': 7, 'without_charger': 10},
            '3': {'name': 'Medium Battery', 'with_charger': 10, 'without_charger': 15},
            '4': {'name': 'Large Battery', 'with_charger': 15, 'without_charger': 20},
            '5': {'name': 'Laptop', '65w+': 20, '65w-': 15, 'without_charger': 25},
            '6': {'name': 'PowerBank', 'price': 10},
            '7': {'name': 'Other Device', 'custom': True}
        }

    def _get_today_file(self):
        """Generate today's data file path"""
        today = datetime.date.today().isoformat()
        return os.path.join(self.DATA_DIR, f"clients_{today}.json")

    def _load_data(self):
        """Load data from JSON file"""
        file_path = self._get_today_file()
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error reading file: {e}")
            return {}

    def _save_data(self, data):
        """Save data to JSON file"""
        try:
            with open(self._get_today_file(), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    def _validate_input(self, prompt, valid_choices):
        """Validate user input against allowed choices"""
        while True:
            choice = input(prompt).strip()
            if choice in valid_choices:
                return choice
            print("Invalid input! Please try again.")

    def add_client(self):
        """Add new client with devices"""
        print("\n--- Add New Client ---")
        name = input("Client name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return

        devices = []
        total_price = 0

        while True:
            print("\nSelect device type:")
            for num, device in self.DEVICE_TYPES.items():
                print(f"{num}. {device['name']}")

            choice = self._validate_input(
                "Enter device number (1-7): ",
                list(self.DEVICE_TYPES.keys())
            )

            device_info = self.DEVICE_TYPES[choice]
            device_name = device_info['name']
            price = 0

            if choice == '5':  # Laptop
                has_charger = self._validate_input(
                    "With charger? (1.Yes 2.No): ",
                    ['1', '2']
                )
                if has_charger == '1':
                    wattage = self._validate_input(
                        "65W+ charger? (1.Yes 2.No): ",
                        ['1', '2']
                    )
                    device_name += " with " + ("65W+" if wattage == '1' else "65W-") + " charger"
                    price = device_info['65w+'] if wattage == '1' else device_info['65w-']
                else:
                    device_name += " without charger"
                    price = device_info['without_charger']

            elif choice == '6':  # PowerBank
                price = device_info['price']

            elif choice == '7':  # Other device
                device_name = input("Device name: ")
                price = int(input("Charging price: "))
                
            else:  # Other devices
                has_charger = self._validate_input(
                    "With charger? (1.Yes 2.No): ",
                    ['1', '2']
                )
                device_name += " with charger" if has_charger == '1' else " without charger"
                price = device_info['with_charger'] if has_charger == '1' else device_info['without_charger']

            devices.append(device_name)
            total_price += price

            if self._validate_input("Add another device? (1.Yes 2.No): ", ['1', '2']) == '2':
                break

        client_data = {
            'name': name,
            'devices': devices,
            'price': total_price,
            'checkout': False,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if self._validate_input(f"Confirm adding client {name}? (1.Yes 2.No): ", ['1', '2']) == '1':
            data = self._load_data()
            client_id = str(len(data) + 1)
            data[client_id] = client_data
            
            if self._save_data(data):
                print(f"\nClient added successfully! ID: {client_id}")
                print(f"Devices: {', '.join(devices)}")
                print(f"Total amount: {total_price} NIS")
            else:
                print("Error saving data!")
            
            input("\nPress Enter to continue...")

    def find_client(self):
        """Search for client by ID"""
        print("\n--- Client Search ---")
        data = self._load_data()
        client_id = input("Client ID: ").strip()

        if client_id not in data:
            print("Client not found!")
            input("\nPress Enter to continue...")
            return

        client = data[client_id]
        print(f"\nName: {client['name']}")
        print(f"Devices: {', '.join(client['devices'])}")
        print(f"Amount: {client['price']} NIS")
        print(f"Time: {client['timestamp']}")

        if not client['checkout']:
            if self._validate_input("Mark as delivered? (1.Yes 2.No): ", ['1', '2']) == '1':
                client['checkout'] = True
                self._save_data(data)
                print("Devices marked as delivered!")
        else:
            print("Already delivered")

        input("\nPress Enter to continue...")

    def daily_report(self):
        """Generate daily profit report"""
        print("\n--- Daily Report ---")
        data = self._load_data()
        
        total = 0
        pending = 0
        device_stats = defaultdict(int)

        for client in data.values():
            if client['checkout']:
                total += client['price']
            else:
                pending += client['price']
            
            for device in client['devices']:
                device_stats[device] += 1

        print(f"Total profit: {total} NIS")
        print(f"Pending amount: {pending} NIS")
        
        print("\nDevices charged today:")
        for device, count in device_stats.items():
            print(f"- {device}: {count}")

        input("\nPress Enter to continue...")

    def main_menu(self):
        """Main menu interface"""
        while True:
            print("\n--- Charging Point Management System ---")
            print("1. Add New Client")
            print("2. Find Client")
            print("3. Daily Report")
            print("4. Exit")

            choice = self._validate_input("Select option (1-4): ", ['1', '2', '3', '4'])

            if choice == '1':
                self.add_client()
            elif choice == '2':
                self.find_client()
            elif choice == '3':
                self.daily_report()
            elif choice == '4':
                if self._validate_input("Confirm exit? (1.Yes 2.No): ", ['1', '2']) == '1':
                    print("Goodbye!")
                    break

if _name_ == "_main_":
    system = ChargingPointSystem()
    system.main_menu()
