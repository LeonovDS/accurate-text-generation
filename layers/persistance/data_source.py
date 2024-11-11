from abc import ABC, abstractmethod
from model.block import BlockWithEmbedding


class DataSource(ABC):
    @abstractmethod
    def get_blocks(self) -> list[BlockWithEmbedding]:
        pass
