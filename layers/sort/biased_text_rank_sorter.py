import numpy as np

from layers.sort.block_sorter import BlockSorter
from layers.embedding.embedding import Embedding
from model.block import BlockWithEmbedding, Block


class BiasedTextRankSorter(BlockSorter):
    def __init__(self, bias_coefficient: float = 0.85):
        self.__bias_coefficient = bias_coefficient

    def __calculate_wx_matrix(self, embedding: Embedding, blocks: list[BlockWithEmbedding]) -> np.ndarray:
        n = len(blocks)
        weights = embedding.pairwise_similarity(blocks)
        weights_sums = [np.sum(row) for row in weights]
        wx = np.array(
            [[weights[j][i] / weights_sums[j] for j in range(n)] for i in range(n)]
        )
        return wx

    def sort(self, embedding: Embedding, blocks: list[BlockWithEmbedding], query: str = None) -> \
            list[BlockWithEmbedding]:
        n = len(blocks)
        btr = np.transpose(np.ones((n,)) / n)
        wx = self.__calculate_wx_matrix(embedding, blocks)
        bias = np.transpose(np.ones((n,)))
        if query is not None:
            query_block = embedding.transform_single(Block(query, 0))
            bias = np.transpose(
                np.array([embedding.similarity(query_block, block) for block in blocks]))
        for i in range(20):
            btr = (1 - self.__bias_coefficient) * bias + self.__bias_coefficient * wx @ btr

        return list(map(lambda it: it[1], sorted(zip(btr, blocks), key=lambda it: it[0])))
