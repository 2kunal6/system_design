from ParkingSpot import ParkingSpot
from Booking import Booking
from Vehicle import Vehicle

class ParkingLot:
    def __init__(self, size):
        self.parking_spots = []
        self.bookings = {}
        for i in range(size):
            self.parking_spots.append(ParkingSpot(i))

    def book_spot(self, vehicle_id, entry_time):
        for spot in self.parking_spots:
            if(spot.id not in self.bookings):
                self.bookings[spot.id] = Booking(spot.id, entry_time, vehicle_id)
                print(f'Booked {spot.id}')
                break

    def unbook_spot(self, vehicle_id, exit_time):
        for k in self.bookings:
            if(self.bookings[k].vehicle_id == vehicle_id):
                self.bookings[k].exit_time = exit_time
                print(f'unbooked {self.bookings[k].parking_spot_id}')
                break

parking_lot = ParkingLot(5)
vehicle_1 = Vehicle(1)
parking_lot.book_spot(vehicle_1.id, 1)
parking_lot.unbook_spot(vehicle_1.id, 2)