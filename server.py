from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from urllib3 import request

from layers.embedding.sentence_transformer_embedding import SentenceTransformerEmbedding
from layers.experiment.experiment import EmbeddingTopOneExperiment
from layers.loading.filtering_book_loader import FilteringBookLoader
from layers.model.configuration import Configuration
from layers.segmentation.block_segmenter import BlockSegmenter

experiments = {
    "embedding-top-one": EmbeddingTopOneExperiment(),
}

configurations = {
    "block-senetence-transformer-1000": Configuration(
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
    ),
    "block-senetence-transformer-2000": Configuration(
        loading=FilteringBookLoader([
            lambda book: "Роулинг" in book.author,
            lambda book: "Филосовский" in book.title,
        ]),
        segmentation=BlockSegmenter(block_max_length=2000),
        embedding=SentenceTransformerEmbedding(
            lambda: SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device='cuda')
        ),
        sorter=None,
        prompt_builder=None,
        inference=None,
    ),
}
app = FastAPI()
templates = Jinja2Templates(directory="static")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "configs": configurations.keys(),
            "experiments": experiments.keys(),
        },
    )


class FormParams(BaseModel):
    experiment: str
    config_a: str
    config_b: str
    input: str


@app.post("/generate")
def generate(request: Request, form: Annotated[FormParams, Body()]):
    res_a: str = experiments[form.experiment].run(configurations[form.config_a], form.input)
    res_b: str = experiments[form.experiment].run(configurations[form.config_b], form.input)
    res_a: list[str] = res_a.split('\n')
    res_b: list[str] = res_b.split('\n')
    print('--------' + str(len(res_a)))
    print('--------' + str(len(res_b)))
    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "answer_a": res_a,
            "answer_b": res_b,
        }
    )


@app.get("/vote")
def vote(winner: str):
    print(winner)
    return "ok"
