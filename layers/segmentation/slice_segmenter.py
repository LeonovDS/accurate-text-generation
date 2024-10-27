from abc import ABC, abstractmethod
from typing import Iterator


class SliceSegmenter(ABC):
    @abstractmethod
    def process(self, text: str) -> Iterator[tuple[int, int]]:
        pass


class SentenceSliceSegmenter(SliceSegmenter):
    def process(self, text: str) -> Iterator[tuple[int, int]]:
        left = 0
        for right, char in enumerate(text):
            if char in '.!?\n':
                yield left, right + 1
                left = right + 1


class ParagraphSliceSegmenter(SliceSegmenter):
    def process(self, text: str) -> Iterator[tuple[int, int]]:
        left = 0
        for right, char in enumerate(text):
            if char == '\n':
                yield left, right + 1
                left = right + 1


class BlockSliceSegmenter(SliceSegmenter):
    def __init__(self, block_max_length: int = 2000):
        self.block_max_length = block_max_length

    def __split_by(self, text: str, left: int, right: int, delimiter: list[str]) -> Iterator[tuple[int, int]]:
        i_left = left
        i_right = left
        while i_right < right:
            while i_left < right and (text[i_left] in delimiter or text[i_left] == ' '):
                i_left += 1
            if i_left == right:
                break
            i_right = i_left
            while i_right < right and text[i_right] not in delimiter:
                i_right += 1
            print(i_left, i_right)
            yield i_left, i_right
            i_left = i_right

    def __group_dialogues(self, text: str, paragraphs: Iterator[tuple[int, int]]) -> Iterator[tuple[int, int]]:
        dialogue: tuple[int, int] | None = None
        for paragraph in paragraphs:
            if text[paragraph[0]] == '-':
                if dialogue is None:
                    dialogue = paragraph
                else:
                    dialogue = dialogue[0], paragraph[1]
            else:
                if dialogue is not None:
                    yield dialogue
                    dialogue = None
                yield paragraph

    def __split_by_blocks(
            self,
            paragraphs: Iterator[tuple[int, int]],
            first_block: tuple[int, int] | None = None
    ) -> Iterator[tuple[int, int]]:
        block: tuple[int, int] = first_block
        if block is None:
            block: tuple[int, int] = next(paragraphs)
        for paragraph in paragraphs:
            if paragraph[0] == paragraph[1]:
                continue
            if paragraph[1] - paragraph[0] > self.block_max_length:
                sentences = self.__split_by(text, paragraph[0], paragraph[1], ['.', '?', '!'])
            elif paragraph[1] - block[0] <= self.block_max_length:
                block = block[0], paragraph[1]
            else:
                yield block
                block = paragraph

    def process(self, text: str) -> Iterator[tuple[int, int]]:
        return self.__group_dialogues(text, self.__split_by(text, 0, len(text), ['\n']))


text = open(
    '/home/yshmgrt/Programming/the-dialogue-system/data/Василий Панфилов/Панфилов В. - Эльф из погранвойск. Кн.1.txt',
    'r').read()
for i in list(BlockSliceSegmenter().process(text))[:30]:
    print(text[i[0]:i[1]])
    print('--------------------------')
