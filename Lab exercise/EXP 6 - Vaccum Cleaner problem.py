def vacuum_cleaner():
    rooms = {
        'A': 'Dirty',
        'B': 'Dirty'
    }

    location = 'A'

    print("Initial State:", rooms)
    print("Vacuum Cleaner starts at Room", location)

    while 'Dirty' in rooms.values():
        if rooms[location] == 'Dirty':
            print("Room", location, "is Dirty. Cleaning...")
            rooms[location] = 'Clean'
        else:
            print("Room", location, "is Clean.")

        if location == 'A':
            location = 'B'
        else:
            location = 'A'

    print("\nFinal State:", rooms)
    print("All rooms are clean!")
    print("Goal State Achieved.")

vacuum_cleaner()
