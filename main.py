from metro_system import MetroSystem

def main():
    metro = MetroSystem()
    metro.load_data()

    while True:
        print("\nWashington Metro Ticket System")
        print("1. View all stations")
        print("2. Purchase ticket")
        print("3. View purchased tickets")
        print("4. Visualize metro map")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            metro.list_stations()

        elif choice == '2':
            src = input("Enter source station ID: ").strip().upper()
            dest = input("Enter destination station ID: ").strip().upper()

            if not src.startswith("S"):
                src = "S" + src
            if not dest.startswith("S"):
                dest = "S" + dest

            if src not in metro.stations or dest not in metro.stations:
                print("Invalid station ID(s).")
                continue

            metro.purchase_ticket(src, dest)

        elif choice == '3':
            metro.view_tickets()

        elif choice == '4':
            metro.visualize()

        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
