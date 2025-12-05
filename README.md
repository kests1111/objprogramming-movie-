# objprogramming-movie-
A simple project to demonstrate class interaction in OOP.
Installation
Only Python 3.8+ needed, no external libraries required.

python main_demo.py

File Structure

models.py - Classes: Movie, Theater, Booking, Seat
booking.py - BookingManager for handling reservations
payments.py - PaymentProcessor for payment simulation
movies_loader.py - JSON file loader
movies.json - Movie database
main_demo.py - Demo program


Usage Examples

Run the demo:
python main_demo.py


Add Your Own Movie

Open movies.json and add:

{
  "movie_id": 6,
  "title": "Your Movie",
  "duration": 120,
  "rating": 8.0,
  "genre": "Genre"
}
