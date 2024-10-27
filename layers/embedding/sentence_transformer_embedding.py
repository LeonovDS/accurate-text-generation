from typing import cast, Callable

from numpy import ndarray
from sentence_transformers import SentenceTransformer
from torch import Tensor

from layers.embedding.embedding import Embedding
from layers.model.block import Block, BlockWithEmbedding


class SentenceTransformerEmbedding(Embedding):
    def __init__(self, model: Callable[[], SentenceTransformer]):
        self.__model = None
        self.__model_factory = model

    def _on_enter(self):
        self.__model = self.__model_factory()
        return self

    def _on_exit(self):
        if self.__model is not None:
            del self.__model

    def transform(self, src: list[Block]) -> list[BlockWithEmbedding]:
        texts = [block.text for block in src]
        embeddings: ndarray = cast(ndarray, self.__model.encode(texts))
        return list(zip(src, embeddings))

    def similarity(self, a: BlockWithEmbedding, b: BlockWithEmbedding) -> float:
        return cast(float, self.__model.similarity(a[1], b[1])[0][0])

    def pairwise_similarity(self, blocks: list[BlockWithEmbedding]) -> Tensor:
        blocks = map(lambda block: block[1], blocks)
        return self.__model.similarity_pairwise(blocks, blocks)
