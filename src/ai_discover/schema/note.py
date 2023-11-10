import abc
from typing import Any

from pydantic import BaseModel

from schema.base import Summary
from schema.bilibili import BiliNoteView


class Note(BaseModel, abc.ABC):
    view: Any
    summary: Summary


class BilibiliNote(Note):
    view: BiliNoteView


class PostNote(Note):
    ...