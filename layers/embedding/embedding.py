from abc import ABC, abstractmethod

from torch import Tensor

from model.block import Block, BlockWithEmbedding


class Embedding(ABC):
    def __enter__(self):
        self._on_enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._on_exit()

    @abstractmethod
    def _on_enter(self):
        pass

    @abstractmethod
    def _on_exit(self):
        pass

    @abstractmethod
    def transform(self, src: list[Block]) -> list[BlockWithEmbedding]:
        pass

    def transform_single(self, src: Block) -> BlockWithEmbedding:
        return self.transform([src])[0]

    @abstractmethod
    def similarity(self, a: BlockWithEmbedding, b: BlockWithEmbedding) -> float:
        pass

    @abstractmethod
    def pairwise_similarity(self, blocks: list[BlockWithEmbedding]) -> Tensor:
        pass
