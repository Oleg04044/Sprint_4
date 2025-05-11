import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    """Базовая фикстура для создания экземпляра BooksCollector."""
    return BooksCollector()

@pytest.fixture
def collector_with_books():
    """Фикстура с предзаполненными книгами без жанров."""
    collector = BooksCollector()
    books = ['Метро 2033', 'Оно', 'Чебурашка', 'Мастер и Маргарита']
    for name in books:
        collector.add_new_book(name)
    return collector

@pytest.fixture
def collector_with_genres(collector_with_books):
    """Фикстура с книгами и установленными жанрами."""
    collector_with_books.set_book_genre('Метро 2033', 'Фантастика')
    collector_with_books.set_book_genre('Оно', 'Ужасы')
    collector_with_books.set_book_genre('Чебурашка', 'Мультфильмы')
    return collector_with_books

