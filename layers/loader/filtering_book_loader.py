import os
from typing import Callable, Iterator

from model.book import Book
from layers.loader.book_loader import BookLoader


class FilteringBookLoader(BookLoader):
    def __init__(self, filters: list[Callable[[Book], bool]]):
        self.__filters = filters

    @staticmethod
    def __get_book(path: str, file: str) -> Book:
        parts = path.split('/')[1:]
        author = parts[0]
        series = '/'.join(parts[1:])
        title = file[:-4]
        path = os.path.join(path, file)
        text = open(path, 'r').read()
        return Book(author=author, series=series, title=title, path=path, text=text)

    def read(self, root: str) -> Iterator[Book]:
        for path, dirs, files in os.walk(root):
            for file in files:
                book = self.__get_book(path, file)
                if all(map(lambda f: f(book), self.__filters)):
                    yield book
