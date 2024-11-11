from __future__ import annotations
from abc import ABC, abstractmethod


class InferenceModel(ABC):
    def __enter__(self) -> InferenceModel:
        self._on_enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._on_exit()

    @abstractmethod
    def _on_enter(self):
        pass

    @abstractmethod
    def _on_exit(self):
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
