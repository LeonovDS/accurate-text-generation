from abc import ABC, abstractmethod
from itertools import chain

from layers.model.block import Block
from layers.model.configuration import Configuration


class Experiment(ABC):
    @abstractmethod
    def run(self, configuration: Configuration, inp: str) -> str:
        pass


class EmbeddingTopOneExperiment(Experiment):
    def run(self, configuration: Configuration, inp: str) -> str:
        with configuration.embedding as embedding:
            print("Start experiment")
            print(f"Input: {inp}")
            print("Calculate input embedding")
            input_embedding = embedding.transform_single(Block(position=0, text=inp))
            print("Read books")
            books = list(configuration.loading.read("data/"))
            print(f"Book count: {len(books)}")
            print("Segment books")
            blocks = list(chain.from_iterable(
                map(
                    lambda book: configuration.segmentation.process(book.text),
                    books
                )
            ))
            print(f"Block count: {len(blocks)}")
            print("Calculate book embeddings")
            book_embeddings = embedding.transform(blocks)
            print("Find best book")
            best = max(book_embeddings, key=lambda it: configuration.embedding.similarity(input_embedding, it))
            print(f"Best book: {best[0]}")
            return best[0].text
