from typing import cast, TYPE_CHECKING, Literal

from numpy import ndarray

from layers.embedding.embedding import Embedding

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer
from model.block import Block, BlockWithEmbedding
from torch import Tensor


class SentenceTransformerEmbedding(Embedding):

    def __init__(self, model_name: str, device: Literal['cuda', 'cpu']):
        self.__model = None
        self.__model_name = model_name
        self.__device = device

    def _on_enter(self):
        from sentence_transformers import SentenceTransformer
        self.__model = SentenceTransformer(self.__model_name, device=self.__device)
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
