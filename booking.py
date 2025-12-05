from models import Booking

class BookingManager:
    def __init__(self):
        self.bookings = {}

    def create_booking(self, theater, guest_name, seats):
        
        if not seats or not guest_name:
            return None

       
        booking = Booking(theater, guest_name, seats)

   
        if not booking.validate_seats():
            return None

        # попытка зарезервировать каждое место
        for row, col in seats:
            success = theater.reserve_seat(row, col, booking.booking_id)
            if not success:
                #(откат: освобождаем те места, что успели занять в этом цикле
                current_index = seats.index((row, col))
                for r, c in seats[:current_index]:
                    theater.release_seat(r, c)
                return None

        
        self.bookings[booking.booking_id] = booking
        return booking

    def confirm_booking(self, booking_id, payment_success):
        if booking_id not in self.bookings:
            return False

        booking = self.bookings[booking_id]

        if payment_success:
            return booking.confirm_booking()
        else:
            return booking.cancel_booking()

    def cancel_booking(self, booking_id):
        if booking_id not in self.bookings:
            return False
        return self.bookings[booking_id].cancel_booking()

    def get_booking(self, booking_id):
        return self.bookings.get(booking_id)
