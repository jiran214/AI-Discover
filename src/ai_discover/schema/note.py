import abc
from typing import Any

from pydantic import BaseModel

from schema.base import Summary
from schema.bilibili import BiliNoteView


class Note(BaseModel, abc.ABC):
    view: Any
    summary: Summary

    def get_outline(self, index):
        return self.summary.outlines[index]

    @property
    def namespace(self): return


class BilibiliNote(Note):
    view: BiliNoteView

    @property
    def namespace(self): return self.view.aid


class PostNote(Note):
    ...