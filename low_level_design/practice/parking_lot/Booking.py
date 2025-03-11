class Booking:
    def __init__(self, parking_spot_id, entry_time, vehicle_id):
        self.parking_spot_id = parking_spot_id
        self.entry_time = entry_time
        self.exit_time = None
        self.vehicle_id = vehicle_id

    def set_exit_time(self, exit_time):
        self.exit_time = exit_time