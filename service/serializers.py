from pydantic.main import BaseModel
from typing import Optional, Iterable


class WaterfallModel(BaseModel):
    uid: Optional[str]
    title: Optional[str]
    url: Optional[str]
    summary: Optional[str]
    height: Optional[str]
    width: Optional[str]
    river: Optional[str]
    country: Optional[str]
    region: Optional[str]
    RF_subject: Optional[str]

    def __repr__(self) -> str:
        return f"WaterfallModel({self.uid}{self.title})"
