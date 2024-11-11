from dataclasses import dataclass


@dataclass
class Book:
    author: str
    series: str
    title: str
    path: str
    text: str
