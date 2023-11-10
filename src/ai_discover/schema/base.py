from enum import Enum
from typing import List, ClassVar

from pydantic import BaseModel, Field, field_validator


class TextType(Enum):
    fragment = "Fragment"
    outline = "Outline"
    summary = "Summary"


class Document(BaseModel):
    content: str
    metadata: dict = Field(default_factory=dict)
    type: ClassVar

    @field_validator('metadata')
    @classmethod
    def metadata_update(cls, v: dict):
        v['type'] = cls.type
        return v


class Fragment(Document):
    type: ClassVar = TextType.fragment.value


class Outline(Document):
    fragments: List[Fragment]
    type: ClassVar = TextType.outline.value


class Summary(Document):
    outlines: List[Outline]
    type: ClassVar = TextType.summary.value

    def get_docs(self):
        docs = [self, self.outlines]
        for outline in self.outlines:
            docs.extend(outline.fragments)


print(Document(content='1').metadata)