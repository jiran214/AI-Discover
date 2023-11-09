import abc
from typing import Any

from pydantic import BaseModel

from schema.bilibili import BiliNoteView, VideoSummary


class Note(BaseModel, abc.ABC):
    view: Any
    summary: Any


class BilibiliNote(Note):
    view: BiliNoteView
    summary: VideoSummary


class PostNote(Note):
    ...