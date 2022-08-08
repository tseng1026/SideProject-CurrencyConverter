from abc import ABC, abstractclassmethod
from typing import List

from app.schemas import Currency


class CurrencyDispatcher(ABC):
    @abstractclassmethod
    def get_currencies(self) -> List[Currency]:
        raise Exception("Undefined get_currencies method")

    @abstractclassmethod
    def get_currency(self, code: str) -> Currency:
        raise Exception("Undefined get_currency method")
