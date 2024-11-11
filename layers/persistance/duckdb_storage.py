from typing import Optional

import duckdb
from duckdb.duckdb import DuckDBPyConnection

from model.block import BlockWithEmbedding, Block
from model.book import Book
from layers.persistance.storage import Storage


class DuckDBStorage(Storage):
    def __init__(self, file: str):
        self.file = file
        self.connection: Optional[DuckDBPyConnection] = None

    def _on_enter(self):
        self.connection = duckdb.connect(self.file)
        self.__init_db()

    def _on_exit(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def add_book(self, book: Book, blocks: list[BlockWithEmbedding]):
        result = self.connection.execute("""
            INSERT INTO books (author, series, path, title) VALUES (?, ?, ?, ?) RETURNING id;
        """, (book.author, book.series, book.path, book.title))
        book_id = result.fetchone()[0]
        for block in blocks:
            self.connection.execute("""
                INSERT INTO blocks (book_id, text, index, embedding) VALUES (?, ?, ?, ?);
            """, (book_id, block[0].text, block[0].position, block[1]))

    def __init_db(self):
        self.connection.execute("""
            INSTALL json;
            LOAD json;
            
            CREATE SEQUENCE IF NOT EXISTS book_ids START 1;
            CREATE SEQUENCE IF NOT EXISTS block_ids START 1;
            
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('book_ids'),
                author TEXT NOT NULL,
                series TEXT NOT NULL,
                path TEXT NOT NULL,
                title TEXT NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS blocks (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('block_ids'),
                book_id INTEGER NOT NULL REFERENCES books(id),
                text TEXT NOT NULL,
                index INTEGER NOT NULL,
                embedding FLOAT[] NOT NULL,
            );
        """)

    def get_blocks(self) -> list[BlockWithEmbedding]:
        result = self.connection.execute("SELECT (text, index, embedding) FROM blocks;")
        return list(map(lambda row: (Block(row[0][0], row[0][1]), row[0][2]), result.fetchall()))

if __name__ == "__main__":
    with DuckDBStorage("../../data.db") as storage:
        print(storage.get_blocks())
