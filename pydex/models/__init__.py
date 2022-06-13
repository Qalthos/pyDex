from pydantic import BaseModel


class Pointer(BaseModel):
    name: str
    url: str


class Language(Pointer):
    pass


class Name(BaseModel):
    language: Language
    name: str

    def __str__(self):
        return self.name
