from abc import ABC, abstractmethod
from model.block import BlockWithEmbedding


class PromptBuilder(ABC):
    @abstractmethod
    def process(self, blocks: list[BlockWithEmbedding], query: BlockWithEmbedding) -> str:
        pass
