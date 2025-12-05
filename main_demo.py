from models import Movie, Theater
from booking import BookingManager
from payments import PaymentProcessor
from movies_loader import MoviesLoader

def demo():
    print("=" * 60)
    print("СИСТЕМА БРОНИРОВАНИЯ БИЛЕТОВ В КИНОТЕАТР")
    print("=" * 60)

    # 1
    loader = MoviesLoader()
    movies_data = loader.load_movies("movies.json")
    
    if not movies_data:
        print("Не удалось загрузить фильмы. Завершение...")
        return
    
  
    loader.display_movies(movies_data)
    print(loader.get_movie_by_id(movies_data, 2))
    # 2.
    selected_movie_data = movies_data[0]
    movie = Movie(
        selected_movie_data['movie_id'],
        selected_movie_data['title'],
        selected_movie_data['duration'],
        selected_movie_data['rating'],
        selected_movie_data['genre']
    )
    print(f"\n Выбран фильм: {movie.title} ({movie.duration} мин, ⭐ {movie.rating})")

    # 3
    theater = Theater(1, movie, "2025-12-01 18:00", 5, 8, 500.0)
    print(f" Зал: {theater.rows}x{theater.cols}, цена: {theater.price_per_seat} тг")
    print(f"  Сеанс: {theater.show_time}")

    # 4. Инициализация менеджера
    manager = BookingManager()

    # 5
    print("\n--- БРОНИРОВАНИЕ 1 ---")
    seats1 = [(1, 1), (1, 2), (1, 3)]
    booking1 = manager.create_booking(theater, "Иван", seats1)
    
    if booking1:
        print(f"  Бронь #{booking1.booking_id}: места {seats1}")
        print(f"  Сумма: {booking1.calculate_total()} тг")
        print(f"  Статус: {booking1.status}")
    else:
        print("✗ Ошибка при бронировании")

    # 6
    print("\n--- ПОПЫТКА ДВОЙНОГО БРОНИРОВАНИЯ ---")
    seats2 = [(1, 2), (1, 4)]
    booking2 = manager.create_booking(theater, "Мария", seats2)
    
    if booking2:
        print(f"✓ Бронь #{booking2.booking_id}: места {seats2}")
    else:
        print("✗ Места недоступны (место (1,2) уже зарезервировано)")

    # 7
    print("\n--- БРОНИРОВАНИЕ 2 ---")
    seats3 = [(2, 1), (2, 2)]
    booking3 = manager.create_booking(theater, "Петр", seats3)
    
    if booking3:
        print(f"✓ Бронь #{booking3.booking_id}: места {seats3}")
        print(f"  Сумма: {booking3.calculate_total()} тг")
    else:
        print("✗ Ошибка при бронировании")

    # 8
    print("\n--- ОБРАБОТКА ПЛАТЕЖЕЙ ---")
    
    if booking1:
        payment_result = PaymentProcessor.process_payment(booking1.total_amount)
        confirmed = manager.confirm_booking(booking1.booking_id, payment_result)
        status = "✓ ПОДТВЕРЖДЕНА" if payment_result and confirmed else "✗ ОТКЛОНЕНА"
        print(f"Бронь #{booking1.booking_id}: {status}")
        booking1_updated = manager.get_booking(booking1.booking_id)
        if booking1_updated:
            print(f"  Статус: {booking1_updated.status}")

    if booking3:
        payment_result = PaymentProcessor.process_payment(booking3.total_amount)
        confirmed = manager.confirm_booking(booking3.booking_id, payment_result)
        status = "✓ ПОДТВЕРЖДЕНА" if payment_result and confirmed else "✗ ОТКЛОНЕНА"
        print(f"Бронь #{booking3.booking_id}: {status}")
        booking3_updated = manager.get_booking(booking3.booking_id)
        if booking3_updated:
            print(f"  Статус: {booking3_updated.status}")

    
    print("\n--- ПЛАН МЕСТ (ОСТАВШИЕСЯ СВОБОДНЫЕ) ---")
    available = theater.get_available_seats()
    print(f"Свободных мест: {len(available)} из {theater.rows * theater.cols}")
    print(f"Свободные места: {available[:15]}...")

    # 10
    if len(movies_data) > 1:
        print("\n--- ПЕРЕКЛЮЧЕНИЕ НА ДРУГОЙ ФИЛЬМ ---")
        second_movie_data = movies_data[1]
        second_movie = Movie(
            second_movie_data['movie_id'],
            second_movie_data['title'],
            second_movie_data['duration'],
            second_movie_data['rating'],
            second_movie_data['genre']
        )
        print(f"✓ Загружен новый фильм: {second_movie.title} ({second_movie.genre})")

demo()
