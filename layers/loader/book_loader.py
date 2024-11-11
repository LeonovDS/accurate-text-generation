from abc import ABC, abstractmethod
from typing import Iterator

from model.book import Book


class BookLoader(ABC):
    @abstractmethod
    def read(self, root: str) -> Iterator[Book]:
        pass
