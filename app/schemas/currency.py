from typing import Optional

from pydantic import BaseModel


class Currency(BaseModel):
    code: str = ""
    name: Optional[str] = None
    number: Optional[int] = None
    country: Optional[str] = None
    flag: Optional[str] = None
    symbol: Optional[str] = None
