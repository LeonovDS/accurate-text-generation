from __future__ import annotations
from abc import ABC, abstractmethod

from layers.persistance.data_source import DataSource
from model.book import Book
from model.block import BlockWithEmbedding


class Storage(DataSource, ABC):
    def __enter__(self) -> Storage:
        self._on_enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._on_exit(exc_type, exc_val, exc_tb)

    @abstractmethod
    def _on_enter(self):
        pass

    @abstractmethod
    def _on_exit(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def add_book(self, book: Book, blocks: list[BlockWithEmbedding]):
        pass
