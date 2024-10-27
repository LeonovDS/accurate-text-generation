from json import dumps, loads, dump, load

from sentence_transformers import SentenceTransformer

from layers.embedding.sentence_transformer_embedding import SentenceTransformerEmbedding
from layers.experiment.experiment import EmbeddingTopOneExperiment
from layers.inference.unsloth_inference_model import UnslothInferenceModel
from layers.loading.book_loader import BookLoader
from layers.loading.filtering_book_loader import FilteringBookLoader
from layers.model.configuration import Configuration
from layers.prompt.prompt_builder import QueryOnlyPromptBuilder
from layers.segmentation.block_segmenter import BlockSegmenter
from layers.segmentation.paragraph_segmenter import ParagraphSegmenter
from layers.segmentation.sentence_segmenter import SentenceSegmenter
from layers.sort.biased_text_rank_sorter import BiasedTextRankSorter
from layers.sort.similarity_sorter import SimilaritySorter

# config = open("default-config.toml").read()
config = load(open("default-config.json"))
print(config)


def build_config(config: dict[str, dict[str, any]]) -> Configuration:
    return Configuration(
        loading=build_loading(config["loading"]),
        segmentation=build_segmentation(config["segmentation"]),
        embedding=build_embedding(config["embedding"]),
        sorter=build_sorting(config["sorting"]),
        prompt_builder=build_prompting(config["prompting"]),
        inference=build_inference(config["inference"]),
    )

loading = {
    "load-all": lambda: FilteringBookLoader(filters=[]),
    "load-by-author": lambda author: FilteringBookLoader(filters=[
        lambda book: author in book
    ]),
    "load-by-title": lambda title: FilteringBookLoader(filters=[
        lambda book: title in book
    ])
}


def build_loading(loading_config: dict[str, any]) -> BookLoader:
    return loading[loading_config["type"]](**loading_config["settings"])

segmentation = {
    "block": lambda block_length: BlockSegmenter(block_max_length=block_length),
    "sentence": lambda: SentenceSegmenter(),
    "paragraph": lambda: ParagraphSegmenter()
}


def build_segmentation(segmentation_config):
    return segmentation[segmentation_config["type"]](**segmentation_config["settings"])


embedding = {
    "sentence-transformers": lambda model: SentenceTransformerEmbedding(
        lambda: SentenceTransformer(model_name_or_path=model)
    )
}



def build_embedding(embedding_config):
    return embedding[embedding_config["type"]](**embedding_config["settings"])

sorting = {
    "similarity": lambda: SimilaritySorter(),
    "biased-text-rank": lambda bias: BiasedTextRankSorter(bias_coefficient=bias),
}

def build_sorting(sorting_config):
    return sorting[sorting_config["type"]](**sorting_config["settings"])


prompting = {
    "basic-prompt": lambda: QueryOnlyPromptBuilder()
}

def build_prompting(prompting_config):
    return prompting[prompting_config["type"]](**prompting_config["settings"])

inference = {
    "unsloth": lambda model, max_tokens: UnslothInferenceModel(
        model_name=model,
        output_tokens=max_tokens
    )
}

def build_inference(inference_config):
    return inference[inference_config["type"]](**inference_config["settings"])


if __name__ == "__main__":
    config = loads(open("default-config.json").read())
    EmbeddingTopOneExperiment().run(build_config(config), "Гарри Поттер получил волшебную палочку")
