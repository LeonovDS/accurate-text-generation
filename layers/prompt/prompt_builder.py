from abc import ABC, abstractmethod

from layers.model.block import BlockWithEmbedding


class PromptBuilder(ABC):
    @abstractmethod
    def process(self, blocks: list[BlockWithEmbedding], query: BlockWithEmbedding) -> str:
        pass


class QueryOnlyPromptBuilder(PromptBuilder):
    def process(self, blocks: list[BlockWithEmbedding], query: BlockWithEmbedding) -> str:
        return f"""
        Continue the following text:
        {query[0].text}
        """
