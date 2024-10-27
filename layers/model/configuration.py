from dataclasses import dataclass

from layers.embedding.embedding import Embedding
from layers.inference.inference_model import InferenceModel
from layers.loading.book_loader import BookLoader
from layers.prompt.prompt_builder import PromptBuilder
from layers.segmentation.block_segmenter import BlockSegmenter
from layers.sort.block_sorter import BlockSorter


@dataclass
class Configuration:
    loading: BookLoader
    segmentation: BlockSegmenter
    embedding: Embedding
    sorter: BlockSorter
    prompt_builder: PromptBuilder
    inference: InferenceModel
