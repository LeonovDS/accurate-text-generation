import re

from layers.segmentation.text_segmenter import TextSegmenter


class BlockSegmenter(TextSegmenter):
    end_of_sentence: re.Pattern[str] = re.compile(r'[.!?\n]')
    dialogue_separator: re.Pattern[str] = re.compile(r'^-')

    def __init__(self, block_max_length: int = 1000):
        self.__block_max_length = block_max_length

    def _process(self, text: str) -> list[str]:
        paragraphs: list[str] = self.__split_by_paragraphs(text)
        paragraphs: list[str] = self.__group_dialogues(paragraphs)
        blocks: list[str] = self.__split_by_blocks(paragraphs)
        return blocks

    @staticmethod
    def __split_by_paragraphs(text: str) -> list[str]:
        lines: list[str] = text.split('\n')
        strip_lines: map = map(lambda line: line.strip(), lines)
        return list(filter(lambda line: len(line) > 0, strip_lines))

    def __group_dialogues(self, lines: list[str]) -> list[str]:
        result: list[str] = []
        for line in lines:
            if len(result) == 0:
                result.append(line)
            elif self.dialogue_separator.match(line) and self.dialogue_separator.match(result[-1]):
                result[-1] += '\n' + line
            else:
                result.append(line)
        return result

    def __split_by_blocks(self, paragraphs: list[str]) -> list[str]:
        blocks: list[str] = ['']
        for paragraph in paragraphs:
            paragraph: str = paragraph.strip()
            if len(paragraph) == 0:
                continue
            if len(paragraph) > self.__block_max_length:
                add_blocks = self.__split_paragraph_by_blocks(paragraph, blocks[-1])
                blocks.pop()
                blocks.extend(add_blocks)
            elif len(blocks[-1]) + len(paragraph) + 1 <= self.__block_max_length:
                blocks[-1] += '\n' + paragraph
            else:
                blocks.append(paragraph)

        return blocks

    def __split_paragraph_by_blocks(self, paragraph: str, last_block: str) -> list[str]:
        blocks: list[str] = [last_block + '\n']
        for sentence in self.end_of_sentence.split(paragraph):
            sentence: str = sentence.strip()
            if len(sentence) == 0:
                continue
            if len(sentence) > self.__block_max_length:
                blocks.append(sentence)
            elif len(blocks[-1]) + len(sentence) + 1 <= self.__block_max_length:
                blocks[-1] += ' ' + sentence
            else:
                blocks.append(sentence)
        return blocks
