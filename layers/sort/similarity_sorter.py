from layers.sort.block_sorter import BlockSorter
from layers.embedding.embedding import Embedding
from model.block import BlockWithEmbedding, Block


class SimilaritySorter(BlockSorter):
    def sort(self, embedding: Embedding, blocks: list[BlockWithEmbedding], query: str) -> list[
        BlockWithEmbedding]:
        query_block = embedding.transform_single(Block(query, 0))
        def key(block: BlockWithEmbedding) -> float:
            return embedding.similarity(block, query_block)

        return sorted(blocks, key=key)
