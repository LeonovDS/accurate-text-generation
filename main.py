from sentence_transformers import SentenceTransformer

from layers.embedding.sentence_transformer_embedding import SentenceTransformerEmbedding
from layers.experiment.experiment import EmbeddingTopOneExperiment
from layers.loading.filtering_book_loader import FilteringBookLoader
from layers.model.configuration import Configuration
from layers.segmentation.block_segmenter import BlockSegmenter

if __name__ == "__main__":
    configuration = Configuration(
        loading=FilteringBookLoader([
            lambda book: "Роулинг" in book.author,
            lambda book: "Филосовский" in book.title,
        ]),
        segmentation=BlockSegmenter(block_max_length=1000),
        embedding=SentenceTransformerEmbedding(
            lambda: SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device='cuda')
        ),
        sorter=None,
        prompt_builder=None,
        inference=None,
    )
    experiment = EmbeddingTopOneExperiment()
    experiment.run(configuration, "Гарри Поттер получил волшебную палочку")
