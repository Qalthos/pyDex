from pydantic import BaseModel

from pydex.models import Name
from .region import Region
from .pokemon import Pokemon


class Generation(BaseModel):
    number: int
    main_region: Region
    name: str
    names: list[Name]
    pokemon_species: list[Pokemon]

    def english_name(self) -> str:
        for name in self.names:
            if name.language.name == "en":
                return name.name
        else:
            return "No english name"
