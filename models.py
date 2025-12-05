
class SeatStatus:
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    SOLD = "SOLD"

class BookingStatus:
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class Movie:
    def __init__(self, movie_id, title, duration, rating, genre):
        self.movie_id = movie_id
        self.title = title
        self.duration = duration  # минуты (int)
        self.rating = rating
        self.genre = genre

    def get_info(self):
        return {
            'id': self.movie_id,
            'title': self.title,
            'duration': self.duration,
            'rating': self.rating,
            'genre': self.genre
        }

class Seat:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.status = SeatStatus.AVAILABLE
        self.booking_id = None

    def mark_reserved(self, booking_id):
        if self.status != SeatStatus.AVAILABLE:
            return False
        self.status = SeatStatus.RESERVED
        self.booking_id = booking_id
        return True

    def mark_sold(self):
        self.status = SeatStatus.SOLD

    def mark_available(self):
        self.status = SeatStatus.AVAILABLE
        self.booking_id = None

    def is_seat_available(self):
        return self.status == SeatStatus.AVAILABLE

class Theater:
    def __init__(self, theater_id, movie, show_time, rows, cols, price_per_seat):
        self.theater_id = theater_id
        self.movie = movie
        self.show_time = show_time  # теперь просто строка
        self.rows = rows
        self.cols = cols
        self.price_per_seat = price_per_seat
        self.seats = self._init_seats()

    def _init_seats(self):
        seats = {}
        for row in range(1, self.rows + 1):
            for col in range(1, self.cols + 1):
                seats[(row, col)] = Seat(row, col)
        return seats

    def reserve_seat(self, row, col, booking_id):
        if (row, col) not in self.seats:
        
            print(f"Ошибка: Место ({row}, {col}) не существует")
            return False
        return self.seats[(row, col)].mark_reserved(booking_id)

    def release_seat(self, row, col):
        if (row, col) in self.seats:
            self.seats[(row, col)].mark_available()
            return True
        return False

    def is_seat_available(self, row, col):
        if (row, col) not in self.seats:
            return False
        return self.seats[(row, col)].is_seat_available()

    def get_available_seats(self):
        available = []
        # dict.items() возвращает пары (ключ, значение)
        for key in self.seats:
            seat = self.seats[key]
            if seat.is_seat_available():
                available.append(key)
        return available

class Booking:
    _booking_counter = 0

    def __init__(self, theater, guest_name, seats):
        Booking._booking_counter += 1
        self.booking_id = Booking._booking_counter
        self.theater = theater
        self.guest_name = guest_name
        self.seats = seats
        self.status = BookingStatus.PENDING
        self.total_amount = len(seats) * theater.price_per_seat
        self.created_at = "Сейчас"  #строка вместо datetime.now()

    def calculate_total(self):
        return self.total_amount

    def confirm_booking(self):
        if self.status != BookingStatus.PENDING:
            return False
        self.status = BookingStatus.CONFIRMED
        for row, col in self.seats:
            self.theater.seats[(row, col)].mark_sold()
        return True

    def cancel_booking(self):
        if self.status == BookingStatus.CONFIRMED:
            return False
        self.status = BookingStatus.CANCELLED
        for row, col in self.seats:
            self.theater.release_seat(row, col)
        return True

    def validate_seats(self):
        for row, col in self.seats:
            if not self.theater.is_seat_available(row, col):
                return False
        return True
