import pytest
from main import BooksCollector

class TestBooksCollector:

    # 1. Тестируем add_new_book (Параметризация: позитивные граничные значения и негативный кейс)
    @pytest.mark.parametrize(
        'book_name, expected_count',
        [
            ('А', True),                                     # Минимальная длина имени
            ('Приключения Алисы в Стране чудес. Сказка', True), # Граничное значение: 40 символов
            ('Приключения Алисы в Стране чудес. Сказка!', False) # Негативный кейс: 41 символ
        ]
    )
    def test_add_new_book_different_lengths(self, collector, book_name, expected_count):
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == expected_count

    # 2. Тестируем add_new_book (Повторное добавление одной и той же книги)
    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book('Кот в сапогах')
        collector.add_new_book('Кот в сапогах')
        assert len(collector.get_books_genre()) == 1

    # 3. Тестируем set_book_genre и get_book_genre (Позитивный сценарий)
    def test_set_book_genre_successfully(self, collector):
        collector.add_new_book('Дракула')
        collector.set_book_genre('Дракула', 'Ужасы')
        assert collector.get_book_genre('Дракула') == 'Ужасы'

    # 4. Тестируем set_book_genre (Попытка установить несуществующий жанр)
    def test_set_book_genre_not_in_list_remains_empty(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фэнтази') # Жанра нет в списке genre
        assert collector.get_book_genre('Гарри Поттер') == ''

    # 5. Тестируем get_books_with_specific_genre
    def test_get_books_with_specific_genre_returns_book(self, collector):
        collector.add_new_book('Десять негритят')
        collector.set_book_genre('Десять негритят', 'Детективы')
    
        assert collector.get_books_with_specific_genre('Детективы') == ['Десять негритят']

    # 6. Тестируем get_books_genre
    def test_get_books_genre_returns_full_dictionary(self, collector):
        collector.add_new_book('Шерлок Холмс')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        current_detective = collector.get_books_genre()
        assert current_detective == {'Шерлок Холмс': 'Детективы'}

    # 7. Тестируем get_books_for_children (Параметризация: жанры с ограничением и без)
    @pytest.mark.parametrize(
        'book_name, genre, is_for_children',
        [
            ('Колобок', 'Мультфильмы', True),   # Нет в genre_age_rating
            ('Оно', 'Ужасы', False),            # Есть в genre_age_rating
            ('Шерлок', 'Детективы', False)       # Есть в genre_age_rating
        ]
    )
    def test_get_books_for_children_filtering(self, collector, book_name, genre, is_for_children):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        children_books = collector.get_books_for_children()
        assert (book_name in children_books) == is_for_children

    # 8. Тестируем add_book_in_favorites и get_list_of_favorites_books
    def test_add_book_in_favorites_successfully(self, collector):
        collector.add_new_book('Властелин Колец')
        collector.add_book_in_favorites('Властелин Колец')
        assert collector.get_list_of_favorites_books() == ['Властелин Колец']

    # 9. Тестируем add_book_in_favorites (Негативные кейсы: повторно или книгу не из BooksCollector)
    @pytest.mark.parametrize(
        'book_to_add, setup_book, expected_favorites_count',
        [
            ('Дюна', 'Дюна', 1),       # Попытка добавить одну и ту же книгу дважды (второй раз добавится внутри теста)
            ('Неизвестная', None, 0)   # Попытка добавить книгу, которой вообще нет в словаре collector
        ]
    )
    def test_add_book_in_favorites_constraints(self, collector, book_to_add, setup_book, expected_favorites_count):
        if setup_book:
            collector.add_new_book(setup_book)
            collector.add_book_in_favorites(setup_book) 
            
        collector.add_book_in_favorites(book_to_add) 
        assert len(collector.get_list_of_favorites_books()) == expected_favorites_count

    # 10. Тестируем delete_book_from_favorites
    def test_delete_book_from_favorites_successfully(self, collector):
        collector.add_new_book('Все приключения Шерлока Холмса')
        collector.add_book_in_favorites('Все приключения Шерлока Холмса')
        collector.delete_book_from_favorites('Все приключения Шерлока Холмса')
        assert 'Матрица' not in collector.get_list_of_favorites_books()