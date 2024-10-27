import duckdb

from layers.model.book import Book
from toml_configuration import build_config

from layers.loading.filtering_book_loader import FilteringBookLoader

FILE_NAME = "/data.duckdb"


def create_tables(conn: duckdb.DuckDBPyConnection):
    conn.execute("""
        INSTALL json;
        LOAD json;
        CREATE SEQUENCE IF NOT EXISTS books_id_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS segmentation_configurations_id_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS embedding_configurations_id_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS sorting_configurations_id_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS prompting_configurations_id_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS inference_configurations_id_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS configurations_id_seq START 1;
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('books_id_seq'),
            author TEXT NOT NULL,
            series TEXT NOT NULL,
            path TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
        );
        CREATE TABLE IF NOT EXISTS segmentation_configurations (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('segmentation_configurations_id_seq'),
            settings JSON NOT NULL UNIQUE,
        ); 
        CREATE TABLE IF NOT EXISTS embedding_configurations ( 
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('embedding_configurations_id_seq'),
            settings JSON NOT NULL UNIQUE,
        );
        CREATE TABLE IF NOT EXISTS sorting_configurations (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('sorting_configurations_id_seq'),
            settings JSON NOT NULL UNIQUE,
        );
        CREATE TABLE IF NOT EXISTS prompting_configurations (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('prompting_configurations_id_seq'),
            settings JSON NOT NULL UNIQUE,
        );
        CREATE TABLE IF NOT EXISTS inference_configurations (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('inference_configurations_id_seq'),
            settings JSON NOT NULL UNIQUE,
        );
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('configurations_id_seq'),
            segmentation_configuration_id INTEGER NOT NULL REFERENCES segmentation_configurations(id),
            embedding_configuration_id INTEGER NOT NULL REFERENCES embedding_configurations(id),
            sorting_configuration_id INTEGER NOT NULL REFERENCES sorting_configurations(id),
            prompting_configuration_id INTEGER NOT NULL REFERENCES prompting_configurations(id),
            inference_configuration_id INTEGER NOT NULL REFERENCES inference_configurations(id),
        );
        CREATE VIEW IF NOT EXISTS configurations_json AS
            SELECT conf.id as id, to_json({
                segmentation: seg_conf.settings,
                embedding: emb_conf.settings,
                sorting: sorting_conf.settings,
                prompting: prompt_conf.settings,
                inference: inf_conf.settings
            })
            FROM configurations as conf
            JOIN segmentation_configurations as seg_conf ON conf.segmentation_configuration_id = seg_conf.id
            JOIN embedding_configurations as emb_conf ON conf.embedding_configuration_id = emb_conf.id
            JOIN sorting_configurations as sorting_conf ON conf.sorting_configuration_id = sorting_conf.id
            JOIN prompting_configurations as prompt_conf ON conf.prompting_configuration_id = prompt_conf.id
            JOIN inference_configurations as inf_conf ON conf.inference_configuration_id = inf_conf.id;
        CREATE TABLE IF NOT EXISTS blocks (
            segmentation_configuration_id INTEGER NOT NULL REFERENCES segmentation_configurations(id),
            embedding_configuration_id INTEGER NOT NULL REFERENCES embedding_configurations(id),
            book_id INTEGER NOT NULL REFERENCES books(book_id),
            range_start INTEGER NOT NULL,
            range_end INTEGER NOT NULL,
            embedding FLOAT[]
        );
    """)


def load_books(conn: duckdb.DuckDBPyConnection) -> None:
    books = FilteringBookLoader(filters=[]).read("/home/yshmgrt/Programming/the-dialogue-system/data")
    books = [(book.author, book.series, book.title, book.path) for book in books]
    conn.executemany("INSERT OR IGNORE INTO books(author, series, title, path) VALUES (?, ?, ?, ?)", books)


def save_configuration_part_and_get_id(conn: duckdb.DuckDBPyConnection, conf: dict[str, any], name: str) -> int:
    import json
    dump = json.dumps(conf[name])
    conn.execute(f"""
        INSERT OR IGNORE INTO {name}_configurations(settings) VALUES(?)
    """, (dump,))
    cur = conn.execute(f"""
        SELECT id FROM {name}_configurations WHERE settings = ?; 
    """, (dump,))
    return cur.fetchone()[0]


def add_configuration(conn: duckdb.DuckDBPyConnection, conf: dict[str, any]) -> None:
    ids = tuple(map(lambda name: save_configuration_part_and_get_id(conn, conf, name),
                    ["segmentation", "embedding", "sorting", "prompting", "inference"]))
    conn.execute("""
        INSERT OR IGNORE INTO configurations(
            segmentation_configuration_id,
            embedding_configuration_id,
            sorting_configuration_id,
            prompting_configuration_id,
            inference_configuration_id
       ) 
       VALUES (?, ?, ?, ?, ?);
       """, ids)


def load_configurations(conn: duckdb.DuckDBPyConnection) -> None:
    import tomllib
    config = tomllib.loads(open('/default-config.toml', 'r').read())
    add_configuration(conn, config)

def find_book(conn: duckdb.DuckDBPyConnection, author: str | None, title: str | None):
    query = conn.query("SELECT * from books")
    if author is not None:
        query = query.filter(f"author LIKE '%{author}%'")
    if title is not None:
        query = query.filter(f"title LIKE '%{title}%'")
    return query.pl()

def write_blocks(conn: duckdb.DuckDBPyConnection, conf: dict[str, any], books: list[Book]):
    config = build_config(conf)
    for book in books:
        text = open(book.path, 'r').read()

if __name__ == "__main__":
    with duckdb.connect(FILE_NAME) as db:
        create_tables(db)
        # load_books(db)
        # load_configurations(db)
        print(find_book(db, None, "Гарри Поттер"))
