from typing import Optional

from pydantic import BaseModel


class Currency(BaseModel):
    curr: str = ""
    country: Optional[str] = None
    flag: Optional[str] = None
    symbol: Optional[str] = None
