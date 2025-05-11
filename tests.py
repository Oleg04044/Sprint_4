import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    """Базовая фикстура для создания экземпляра BooksCollector."""
    return BooksCollector()


@pytest.fixture
def collector_with_books():
    """Фикстура с предзаполненными книгами."""
    collector = BooksCollector()
    books = {
        'Метро 2033': 'Фантастика',
        'Оно': 'Ужасы',
        'Чебурашка': 'Мультфильмы',
        'Шерлок Холмс': 'Детективы',
        'Мастер и Маргарита': ''
    }
    for name, genre in books.items():
        collector.add_new_book(name)
        if genre:
            collector.set_book_genre(name, genre)
    return collector


@pytest.fixture
def collector_with_favorites(collector_with_books):
    """Фикстура с книгами в избранном."""
    collector = collector_with_books
    collector.add_book_in_favorites('Метро 2033')
    collector.add_book_in_favorites('Чебурашка')
    return collector


class TestBooksCollector:

    @pytest.mark.parametrize('name, expected', [
        ('Война и мир', True),
        ('1984', True),
        ('', False),
        ('Очень длинное название книги, которое превышает 40 символов', False)
    ], ids=['valid_russian', 'valid_english', 'empty', 'too_long'])
    def test_add_new_book(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    def test_add_existing_book_not_added(self, collector):
        collector.add_new_book('Преступление и наказание')
        collector.add_new_book('Преступление и наказание')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize('name, genre, expected', [
        ('Метро 2033', 'Фантастика', True),
        ('Оно', 'Ужасы', True),
        ('Несуществующая книга', 'Фантастика', False),
        ('Метро 2033', 'Несуществующий жанр', False)
    ])
    def test_set_book_genre(self, collector_with_books, name, genre, expected):
        collector_with_books.set_book_genre(name, genre)
        if expected:
            assert collector_with_books.get_book_genre(name) == genre
        else:
            if name in collector_with_books.get_books_genre():
                assert collector_with_books.get_book_genre(name) != genre

    def test_get_books_with_specific_genre(self, collector_with_books):
        result = collector_with_books.get_books_with_specific_genre('Фантастика')
        assert result == ['Метро 2033']

    def test_get_books_for_children(self, collector_with_books):
        result = collector_with_books.get_books_for_children()
        assert 'Чебурашка' in result
        assert 'Метро 2033' in result
        assert 'Оно' not in result
        assert 'Шерлок Холмс' not in result

    def test_favorites_workflow(self, collector_with_books):
        collector = collector_with_books

        collector.add_book_in_favorites('Мастер и Маргарита')
        assert 'Мастер и Маргарита' in collector.get_list_of_favorites_books()

        collector.add_book_in_favorites('Мастер и Маргарита')
        assert len(collector.get_list_of_favorites_books()) == 1

        collector.delete_book_from_favorites('Мастер и Маргарита')
        assert 'Мастер и Маргарита' not in collector.get_list_of_favorites_books()

    def test_initial_state(self, collector):
        assert collector.get_books_genre() == {}
        assert collector.get_list_of_favorites_books() == []
        assert len(collector.genre) == 5
        assert len(collector.genre_age_rating) == 2

    def test_get_book_genre_for_nonexistent_book(self, collector):
        assert collector.get_book_genre('Несуществующая книга') is None

    def test_add_non_existent_book_to_favorites_not_added(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_max_length_name(self, collector):
        name = 'A' * 40
        collector.add_new_book(name)
        assert name in collector.get_books_genre()