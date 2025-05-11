import pytest
from main import BooksCollector


class TestBooksCollector:

    @pytest.mark.parametrize('name', [
        'Война и мир',
        '1984',
        'Оно',
        pytest.param('', marks=pytest.mark.xfail(reason="Пустое название недопустимо")),
        pytest.param('Очень длинное название книги, которое превышает 40 символов',
                     marks=pytest.mark.xfail(reason="Название >40 символов недопустимо"))
    ])
    def test_add_new_book(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        if 0 < len(name) < 41:
            assert name in collector.get_books_genre()
            assert collector.get_book_genre(name) == ''
        else:
            assert name not in collector.get_books_genre()

    def test_add_existing_book_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Преступление и наказание')
        collector.add_new_book('Преступление и наказание')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize('name,genre', [
        ('Метро 2033', 'Фантастика'),
        ('Оно', 'Ужасы'),
        pytest.param('Несуществующая книга', 'Фантастика',
                     marks=pytest.mark.xfail(reason="Книга должна существовать")),
        pytest.param('Метро 2033', 'Несуществующий жанр',
                     marks=pytest.mark.xfail(reason="Жанр должен быть допустимым"))
    ])
    def test_set_book_genre(self, name, genre):
        collector = BooksCollector()
        collector.add_new_book(name if name != 'Несуществующая книга' else 'Другая книга')
        collector.set_book_genre(name, genre)

        if name in collector.get_books_genre() and genre in collector.genre:
            assert collector.get_book_genre(name) == genre
        else:
            assert collector.get_book_genre(name) != genre

    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        test_data = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Ужасы',
            'Книга 3': 'Фантастика',
            'Книга 4': 'Комедии'
        }

        for name, genre in test_data.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        result = collector.get_books_with_specific_genre('Фантастика')
        assert len(result) == 2
        assert 'Книга 1' in result
        assert 'Книга 3' in result

    def test_get_books_for_children(self):
        collector = BooksCollector()
        test_data = {
            'Чебурашка': 'Мультфильмы',
            'Оно': 'Ужасы',
            'Шерлок Холмс': 'Детективы',
            'Гарри Поттер': 'Фантастика'
        }

        for name, genre in test_data.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        result = collector.get_books_for_children()
        assert 'Чебурашка' in result
        assert 'Гарри Поттер' in result
        assert 'Оно' not in result
        assert 'Шерлок Холмс' not in result

    def test_favorites_workflow(self):
        collector = BooksCollector()
        collector.add_new_book('Мастер и Маргарита')

        collector.add_book_in_favorites('Мастер и Маргарита')
        assert 'Мастер и Маргарита' in collector.get_list_of_favorites_books()

        collector.add_book_in_favorites('Мастер и Маргарита')
        assert len(collector.get_list_of_favorites_books()) == 1

        collector.delete_book_from_favorites('Мастер и Маргарита')
        assert 'Мастер и Маргарита' not in collector.get_list_of_favorites_books()

        collector.delete_book_from_favorites('Несуществующая книга')
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_initial_state(self):
        collector = BooksCollector()
        assert collector.get_books_genre() == {}
        assert collector.get_list_of_favorites_books() == []
        assert len(collector.genre) == 5
        assert len(collector.genre_age_rating) == 2

    def test_get_book_genre_for_nonexistent_book(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Несуществующая книга') is None

    def test_add_non_existent_book_to_favorites_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert len(collector.get_list_of_favorites_books()) == 0