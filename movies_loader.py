import json

class MoviesLoader:
    
    
    @staticmethod
    def load_movies(filename="movies.json"):
        """
        Загрузить фильмы из JSON файла
        
        Args:
            filename: Путь к JSON файлу
            
        Returns:
            Список словарей с фильмами или пустой список при ошибке
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('movies', [])
        except FileNotFoundError:
            print(f"Ошибка: Файл {filename} не найден!")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка: Некорректный JSON формат в {filename}!")
            return []

    @staticmethod
    def get_movie_by_id(movies, movie_id):
        """
        Получить фильм по ID
        
        Args:
            movies: Список фильмов
            movie_id: ID фильма
            
        Returns:
            Словарь с данными фильма или None
        """
        for movie in movies:
            if movie['movie_id'] == movie_id:
                return movie
        return None

    @staticmethod
    def display_movies(movies):
        """Показать все доступные фильмы"""
        if not movies:
            print("Нет доступных фильмов")
            return
        
        print("\n--- Доступные фильмы ---")
        for movie in movies:
            print(f"ID: {movie['movie_id']} | {movie['title']} ({movie['duration']} мин) | ⭐ {movie['rating']} | {movie['genre']}")
