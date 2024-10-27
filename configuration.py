from __future__ import annotations

from dataclasses import dataclass
from typing import Union, Any, Callable, Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from layers.embedding.sentence_transformer_embedding import SentenceTransformerEmbedding
from layers.experiment.experiment import EmbeddingTopOneExperiment
from layers.inference.unsloth_inference_model import UnslothInferenceModel
from layers.loading.filtering_book_loader import FilteringBookLoader
from layers.model.configuration import Configuration
from layers.prompt.prompt_builder import QueryOnlyPromptBuilder
from layers.segmentation.block_segmenter import BlockSegmenter
from layers.segmentation.paragraph_segmenter import ParagraphSegmenter
from layers.segmentation.sentence_segmenter import SentenceSegmenter
from layers.sort.biased_text_rank_sorter import BiasedTextRankSorter
from layers.sort.similarity_sorter import SimilaritySorter


@dataclass(kw_only=True)
class ObjectConfig:
    params: dict[str, Config]


@dataclass(kw_only=True)
class OneOfConfig:
    selected: str
    child: Config


@dataclass(kw_only=True)
class Scheme:
    name: str
    type: str


@dataclass(kw_only=True)
class ObjectScheme(Scheme):
    type: str = "object"
    fields: list[Scheme]
    factory: Callable[[dict[str, any]], any]


@dataclass(kw_only=True)
class OneOfScheme(Scheme):
    type: str = "one_of"
    options: list[Scheme]


@dataclass(kw_only=True)
class IntScheme(Scheme):
    type: str = "int"


@dataclass(kw_only=True)
class StrScheme(Scheme):
    type: str = "str"


type Config = Union[int | str | ObjectConfig | OneOfConfig]


def build_object_from_scheme(scheme: Scheme, config: Config) -> Any:
    if isinstance(scheme, ObjectScheme) and isinstance(config, ObjectConfig):
        args = dict()
        for name, value in config.params.items():
            child = list(filter(lambda param: param.name == name, scheme.fields))[0]
            args[name] = build_object_from_scheme(child, value)
        return scheme.factory(args)
    elif isinstance(scheme, OneOfScheme) and isinstance(config, OneOfConfig):
        selected = list(filter(lambda option: option.name == config.selected, scheme.options))[0]
        return build_object_from_scheme(selected, config.child)
    elif isinstance(scheme, IntScheme) and isinstance(config, int):
        return config
    elif isinstance(scheme, StrScheme) and isinstance(config, str):
        return config
    else:
        raise ValueError(f"Incompatible property and field types: {scheme}, {config}")


config = ObjectScheme(
    name="сonfig",
    fields=[
        OneOfScheme(
            name="loading",
            options=[
                ObjectScheme(
                    name="all-books",
                    fields=[],
                    factory=lambda _: FilteringBookLoader([])
                ),
                ObjectScheme(
                    name="by-author",
                    fields=[
                        StrScheme(name="author")
                    ],
                    factory=lambda d: FilteringBookLoader([
                        lambda book: d["author"] in book.author
                    ])
                ),
                ObjectScheme(
                    name="by-title",
                    fields=[
                        StrScheme(name="title")
                    ],
                    factory=lambda d: FilteringBookLoader([
                        lambda book: d["title"] in book.title
                    ])
                )
            ],
        ),
        OneOfScheme(
            name="segmentation",
            options=[
                ObjectScheme(
                    name="block",
                    fields=[
                        IntScheme(name="block-length")
                    ],
                    factory=lambda d: BlockSegmenter(block_max_length=d["block-length"])
                ),
                ObjectScheme(
                    name="paragraph",
                    fields=[],
                    factory=lambda _: ParagraphSegmenter()
                ),
                ObjectScheme(
                    name="sentence",
                    fields=[],
                    factory=lambda _: SentenceSegmenter()
                )
            ],
        ),
        OneOfScheme(
            name="embedding",
            options=[
                ObjectScheme(
                    name="sentence-transformer",
                    fields=[
                        StrScheme(name="model_name_or_path"),
                        StrScheme(name="device")
                    ],
                    factory=lambda d: SentenceTransformerEmbedding(
                        lambda: SentenceTransformer(**d)
                    )
                ),
            ],
        ),
        OneOfScheme(
            name="sorter",
            options=[
                ObjectScheme(
                    name="similarity",
                    fields=[],
                    factory=lambda _: SimilaritySorter()
                ),
                ObjectScheme(
                    name="biased-text-rank",
                    fields=[
                        IntScheme(name="bias")
                    ],
                    factory=lambda d: BiasedTextRankSorter(
                        bias_coefficient=d["bias"] / 100
                    )
                ),
            ],
        ),
        OneOfScheme(
            name="prompt_builder",
            options=[
                ObjectScheme(
                    name="query-only",
                    fields=[],
                    factory=lambda _: QueryOnlyPromptBuilder(),
                )
            ],
        ),
        OneOfScheme(
            name="inference",
            options=[
                ObjectScheme(
                    name="unsloth",
                    fields=[
                        StrScheme(name="model_name"),
                        IntScheme(name="output_tokens")
                    ],
                    factory=lambda d: UnslothInferenceModel(**d)
                )
            ]
        )
    ],
    factory=lambda d: Configuration(**d)
)

app = FastAPI()


@app.get('/scheme')
def get_scheme():
    return config


class GenerateRequest(BaseModel):
    config: ObjectConfig
    query: str


@app.post('/generate')
def generate(request: Annotated[GenerateRequest, Body()]):
    return EmbeddingTopOneExperiment().run(
        build_object_from_scheme(config, request.config),
        request.query
    )


@app.get('/sample-config')
def sample_config():
    return ObjectConfig(
        params={
            "loading": OneOfConfig(
                selected="by-title",
                child=ObjectConfig(
                    params={
                        "title": "1. Гарри Поттер и Филосовский Камень"
                    }
                )
            ),
            "segmentation": OneOfConfig(
                selected="block",
                child=ObjectConfig(
                    params={
                        "block-length": 2000
                    }
                )
            ),
            "embedding": OneOfConfig(
                selected="sentence-transformer",
                child=ObjectConfig(
                    params={
                        "model_name_or_path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                        "device": "cpu"
                    }
                )
            ),
            "sorter": OneOfConfig(
                selected="similarity",
                child=ObjectConfig(
                    params={}
                )
            ),
            "prompt_builder": OneOfConfig(
                selected="query-only",
                child=ObjectConfig(
                    params={}
                )
            ),
            "inference": OneOfConfig(
                selected="unsloth",
                child=ObjectConfig(
                    params={
                        "model_name": "unsloth/Meta-Llama-3.1-8B",
                        "output_tokens": 512
                    }
                )
            )
        }
    )
