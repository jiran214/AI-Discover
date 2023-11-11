import abc
from typing import List, Literal, Dict, Union

from dataset import Table
from langchain.schema import Document
from langchain.schema.vectorstore import VectorStore
from qdrant_client.http import models as rest
from qdrant_client.http.models import FieldCondition, MatchValue

from schema.base import TextType, Outline, Summary, Fragment
from schema.note import Note


class DocsRetriever(abc.ABC):

    def __init__(self, client: VectorStore):
        self.client = client

    @abc.abstractmethod
    def retrieve(self, *args, **kwargs): ...


class SimpleRetriever(DocsRetriever):
    """条件查找/全部查找"""

    def retrieve(
            self,
            query, k,
            filter_types: List[TextType] = None
            , *args, **kwargs
    ) -> List[Document]:
        metadata_filter = None
        if filter_types:
            metadata_filter = rest.Filter(should=[
                FieldCondition(
                    key="metadata.type",
                    match=MatchValue(value=type.value)
                )
                for type in filter_types
            ])
        found_docs = self.client.similarity_search(query, k=k, filter=metadata_filter, **kwargs)
        return found_docs


class DeepRetriever(DocsRetriever):

    def __init__(
            self, client: VectorStore, query_id=None,
            note_store: Table = None, note_memory: Dict[str, Note] = None
    ):
        super().__init__(client)
        self.query_id = query_id
        self.note_store = note_store
        self.note_memory = note_memory

    def get_note(self, namespace):
        if self.note_memory:
            return self.note_memory.get(namespace)
        res = self.note_store.find_one(query_id=self.query_id, namespace=namespace)
        return Note(**res)

    def retrieve(
            self, query, k,
            parent_type: TextType,
            *args, **kwargs
    ) -> (Dict[str, Note], List[Union[Outline, Summary, Fragment]]):
        docs = SimpleRetriever(self.client).retrieve(query, k, filter_types=[parent_type])
        # 召回子文档
        found_notes_map = {}  # 找到的所有笔记
        result_list = []  # 找到的所有相关笔记片段列表
        for doc in docs:
            namespace = doc.metadata['namespace']
            if namespace in found_notes_map:
                note = found_notes_map[namespace]
            else:
                note = self.get_note(namespace)
                found_notes_map[namespace] = note

            if parent_type == TextType.summary:
                result_list.append(note.summary)
            elif parent_type == TextType.outline:
                index = doc.metadata['index']
                result_list.append(note.get_outline(index))
            else:
                result_list.append(Fragment(content=doc.page_content))
        return found_notes_map, result_list
