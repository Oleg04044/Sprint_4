import pytest
from main import BooksCollector

class TestBooksCollector:
    @pytest.mark.parametrize('name, expected', [
        ('Война и мир', True),
        ('1984', True),
        ('', False),
        ('A' * 41, False)
    ], ids=['valid_name', 'another_valid_name', 'empty_name', 'too_long_name'])
    def test_add_new_book(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    def test_add_existing_book_not_added(self, collector):
        collector.add_new_book('Дубровский')
        collector.add_new_book('Дубровский')
        assert len(collector.get_books_genre()) == 1

    def test_set_valid_genre_for_existing_book(self, collector_with_books):
        collector_with_books.set_book_genre('Метро 2033', 'Фантастика')
        assert collector_with_books.get_book_genre('Метро 2033') == 'Фантастика'

    def test_set_genre_for_nonexistent_book(self, collector):
        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.get_books_genre()

    def test_set_invalid_genre(self, collector_with_books):
        collector_with_books.set_book_genre('Метро 2033', 'Несуществующий жанр')
        assert collector_with_books.get_book_genre('Метро 2033') == ''

    def test_get_genre_for_book_with_genre(self, collector_with_genres):
        assert collector_with_genres.get_book_genre('Метро 2033') == 'Фантастика'

    def test_get_genre_for_book_without_genre(self, collector_with_books):
        assert collector_with_books.get_book_genre('Мастер и Маргарита') == ''

    def test_get_genre_for_nonexistent_book(self, collector):
        assert collector.get_book_genre('Несуществующая книга') is None

    def test_get_books_genre_returns_full_dict(self, collector_with_genres):
        expected = {
            'Метро 2033': 'Фантастика',
            'Оно': 'Ужасы',
            'Чебурашка': 'Мультфильмы',
            'Мастер и Маргарита': ''
        }
        assert collector_with_genres.get_books_genre() == expected

    def test_get_books_with_specific_genre(self, collector_with_genres):
        result = collector_with_genres.get_books_with_specific_genre('Фантастика')
        assert result == ['Метро 2033']

    def test_get_books_for_children(self, collector_with_genres):
        result = collector_with_genres.get_books_for_children()
        assert 'Чебурашка' in result
        assert 'Метро 2033' in result
        assert 'Оно' not in result

    # Тесты для работы с избранным
    def test_add_book_to_favorites(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Метро 2033')
        assert 'Метро 2033' in collector_with_books.get_list_of_favorites_books()

    def test_add_book_to_favorites_twice(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Метро 2033')
        collector_with_books.add_book_in_favorites('Метро 2033')
        assert len(collector_with_books.get_list_of_favorites_books()) == 1

    def test_delete_book_from_favorites(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Метро 2033')
        collector_with_books.delete_book_from_favorites('Метро 2033')
        assert 'Метро 2033' not in collector_with_books.get_list_of_favorites_books()

    def test_add_nonexistent_book_to_favorites(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_initial_state(self, collector):
        assert collector.get_books_genre() == {}
        assert collector.get_list_of_favorites_books() == []
        assert collector.genre == ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        assert collector.genre_age_rating == ['Ужасы', 'Детективы']