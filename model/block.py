from dataclasses import dataclass

from numpy import ndarray


@dataclass
class Block:
    text: str
    position: int

type BlockWithEmbedding = tuple[Block, ndarray]