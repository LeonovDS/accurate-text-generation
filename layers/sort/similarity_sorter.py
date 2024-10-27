from layers.embedding.embedding import Embedding
from layers.model.block import BlockWithEmbedding
from layers.sort.block_sorter import BlockSorter


class SimilaritySorter(BlockSorter):
    def sort(self, embedding: Embedding, blocks: list[BlockWithEmbedding], bias: BlockWithEmbedding) -> list[
        BlockWithEmbedding]:
        def key(block: BlockWithEmbedding) -> float:
            return embedding.similarity(block, bias)

        return sorted(blocks, key=key)
