import json
import datetime
import os
from collections import defaultdict

print('Welcome to the Charging Point Management System!')

def File_Generator():
    """
    Creates a new JSON file for each day's data
    """
    todayS = str(datetime.date.today())
    fileName = f'data/clients_{todayS}.json'
    return fileName

def import_data():
    """
    Imports data from the JSON file
    """
    fileName = File_Generator()
    if not os.path.exists(fileName):
        with open(fileName, 'w', encoding='utf-8') as file:
            json.dump({}, file, indent=4, ensure_ascii=False)
    with open(fileName, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(data):
    """
    Saves client data to JSON file
    """
    fileName = File_Generator()
    with open(fileName, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def Add_New_Client(name, device, price):
    """
    Adds a new client with their devices
    """
    while True:
        print("\nSelect device type:")
        print("1. Mobile Phone")
        print("2. Small Battery")
        print("3. Medium Battery")
        print("4. Large Battery")
        print("5. Laptop")
        print("6. Power Bank")
        print("7. Other Device")
        selection = input("Please select device number to charge: ")
        
        if selection == '6':
            device.append("Power Bank")
            price += 2
            break
        elif selection in ['1', '2', '3', '4', '5']:
            while True:
                print("\nIs the charger included?")
                print("1. Yes")
                print("2. No")
                ans = input("Please select: ")
                
                if ans == '1':
                    if selection == '1':
                        device.append("Mobile Phone with charger")
                        price += 1
                    elif selection == '2':
                        device.append("Small Battery with charger")
                        price += 2
                    elif selection == '5':
                        while True:
                            print("Is your charger 65W or higher?")
                            print("1. Yes")
                            print("2. No")
                            isCharger = input("Please select: ")
                            if isCharger == "1":
                                device.append("Laptop with 65W+ charger")
                                price += 3
                                break
                            elif isCharger == '2':
                                device.append("Laptop with <65W charger")
                                price += 2
                                break
                            else:
                                print("Invalid input! Please choose 1 or 2")
                    elif selection == '3':
                        device.append('Medium Battery with charger')
                        price += 3
                    else:
                        device.append("Large Battery with charger")
                        price += 4
                    break
                elif ans == '2':
                    if selection == '1':
                        device.append("Mobile Phone without charger")
                        price += 2
                    elif selection == '5':
                        device.append("Laptop without charger")
                        price += 4
                    elif selection == '2':
                        device.append("Small Battery without charger")
                        price += 4
                    elif selection == '3':
                        device.append('Medium Battery without charger')
                        price += 5
                    else:
                        device.append("Large Battery without charger")
                        price += 6
                    break
                else:
                    print('\nInvalid input! Please choose the correct option')
            break
        elif selection == '7':
            deviceName = input("Enter device name to charge: ")
            customPrice = int(input('Charging cost: '))
            device.append(deviceName)
            price += customPrice
            break
        else:
            print("\nPlease enter a number between 1-7!")

    while True:
        print("\n1. Yes")
        print("2. No")
        answer = input('Do you want to add another device? ')
        if answer == '1':
            Add_New_Client(name, device, price)
        elif answer == '2':
            clientInfo = {
                'client name': name,
                'devices': device,
                'price': price,
                'checkout': False
            }
            print(f'\nName: {name}')
            print('Devices:', ','.join(device))
            print(f'Charging cost: {price} NIS')
            
            while True:
                print("\n1. Yes")
                print("2. No")
                ans = input(f'Confirm adding {name} to system? ')
                if ans == '1':
                    data = import_data()
                    id = len(data) + 1
                    data[id] = clientInfo
                    save_data(data)
                    print(f'\n{name} added successfully!')
                    print(f"Client ID for {name}: {id}")
                    input("\nPress any key to continue...")
                    main()
                elif ans == "2":
                    main()

def Find_My_Clients():
    data = import_data()
    id = input("Please enter client ID: ")

    if id in data.keys():
        print('Client found!')
        clientInfo = list(data[id].values())
        print(f'\nName: {clientInfo[0]}')
        print('Devices:', ','.join(clientInfo[1]))
        print(f'Total cost: {clientInfo[2]} NIS')

        if clientInfo[-1] == False:
            while True:
                print('\n---Payment---')
                print("\n1. Mark as delivered")
                print("2. Go back")
                print("3. Return to main menu")
                ans = input("Select option: ")
                if ans == '1':
                    fileName = File_Generator()
                    data[id].pop('checkout')
                    data[id]['checkout'] = True
                    save_data(data)
                    print('Delivery completed successfully!')
                    main()
                elif ans == '2':
                    Find_My_Clients()
                elif ans == '3':
                    main()
                else:
                    print("Please choose 1, 2 or 3 only.")
        else:
            print('\nAlready delivered!')
            input('Press any key to return: ')
            main()
    else:
        print("USER NOT FOUND! Please check user ID and try again")
        input('Press any key to go back: ')
        main()

def profit_Tracker():
    data = import_data()
    totalProfit = 0
    pending = 0

    for value in list(data.values()):
        if value['checkout'] == True:
            totalProfit += value['price']
        else:
            pending += value['price']

    print(f'Total profit = {totalProfit} NIS')
    print(f'Pending amount = {pending} NIS')
    input('\n Press any key to return to main menu')
    main()

def main():
    print("\n1. Add new client")
    print("2. Search by client ID")
    print("3. Today's profit")
    print("4. Exit")

    choice = input("\nPlease enter option number: ").strip()
    if choice == '1':
        print('\n---Add Client---')
        name = input("Please enter client name: ").strip()
        device = []
        price = 0
        Add_New_Client(name, device, price)
    elif choice == '2':
        print('\n---Search---')
        Find_My_Clients()
    elif choice == '3':
        print("\n---Today's Profit---")
        profit_Tracker()
    elif choice == '4':
        print("1. Yes")
        print("2. No")
        ans = input('Are you sure? ')

        if ans == '1':
            print("Goodbye!")
            quit()
        elif ans == '2':
            main()
        else:
            print("Invalid input!")
    else:
        print("Invalid input!")
        main()

main()
