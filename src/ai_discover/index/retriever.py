import abc
from typing import List, Literal

from langchain.schema import Document
from langchain.schema.vectorstore import VectorStore

from schema.base import TextType


class DocsRetriever(abc.ABC):

    def __init__(self, client: VectorStore):
        self.client = client

    @abc.abstractmethod
    def retrieve(self, query, k, metadata_filter, **kwargs) -> List[Document]: ...


class SimpleRetriever(DocsRetriever):
    def retrieve(self, query, k, metadata_filter=None, **kwargs) -> List[Document]:
        docs = self.client.similarity_search(query, k=k, filter=metadata_filter, **kwargs)
        return docs


class DeepRetriever(DocsRetriever):
    def retrieve(self, query, k, deep: TextType, metadata_filter=None, **kwargs) -> List[Document]:
        metadata_filter = {}
        docs = self.client.similarity_search(query, k=k, filter=metadata_filter, **kwargs)
        discover_docs = []
        for doc in docs:
            # 找到所有子节点
            ...
        return discover_docs