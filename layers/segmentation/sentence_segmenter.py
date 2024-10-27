import re

from layers.segmentation.text_segmenter import TextSegmenter


class SentenceSegmenter(TextSegmenter):
    end_of_sentence: re.Pattern[str] = re.compile(r'[.!?\n]')

    def _process(self, text: str) -> list[str]:
        return self.end_of_sentence.split(text)
