from layers.segmentation.text_segmenter import TextSegmenter


class ParagraphSegmenter(TextSegmenter):
    def _process(self, text: str) -> list[str]:
        return text.split('\n')
