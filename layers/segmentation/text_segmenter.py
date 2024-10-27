from abc import ABC, abstractmethod

from layers.model.block import Block


class TextSegmenter(ABC):
    def process(self, text: str) -> list[Block]:
        blocks: list[str] = self._process(text)
        blocks: map = map(lambda block: block.strip(), blocks)
        blocks: list[str] = list(filter(lambda block: len(block) > 0, blocks))
        blocks: list[Block] = [Block(sentence, i) for i, sentence in enumerate(blocks)]
        return blocks

    @abstractmethod
    def _process(self, text: str) -> list[str]:
        pass
