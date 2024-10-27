from abc import ABC, abstractmethod


class InferenceModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
