from layers.prompt.prompt_builder import PromptBuilder
from model.block import BlockWithEmbedding


class QueryOnlyPromptBuilder(PromptBuilder):
    def process(self, blocks: list[BlockWithEmbedding], query: BlockWithEmbedding) -> str:
        return f"{query[0].text}"
