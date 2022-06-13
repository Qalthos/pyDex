import requests
from pydantic import BaseModel
from pydantic.tools import parse_obj_as

from pydex.models import Pointer, Name


class Region(BaseModel):
    name: str
    names: list[Name]

    @staticmethod
    def from_pointer(data: Pointer) -> "Region":
        return parse_obj_as(Region, requests.get(data.url).json())
