from abc import ABC, abstractmethod

from layers.embedding.embedding import Embedding
from model.block import BlockWithEmbedding


class BlockSorter(ABC):
    @abstractmethod
    def sort(self, embedding: Embedding, blocks: list[BlockWithEmbedding], query: str) -> list[BlockWithEmbedding]:
        pass
