# Build vectorstore and keep the metadata
from typing import List, Union

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.grpc import VectorParams
from qdrant_client.http.models import Distance

import cfg
import llm
from schema import base


SUMMARY_OUTLINE_MAX_SPLIT = 500
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", " ", ""],
    chunk_size=cfg.chunk_size,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)


def split_text(
        docs: List[Union[Document, base.Fragment, base.Summary, base.Outline]]
) -> List[Document]:
    documents = []
    for doc in docs:
        documents.append(Document(
            page_content=getattr(doc, 'content'),
            metadata=doc.metadata,
        ))
    split_docs = text_splitter.split_documents(documents)
    return split_docs


class VTS(Qdrant):
    _client = {}

    @classmethod
    def get_client(cls, path):
        if path not in cls._client:
            client = QdrantClient(path=path)
            cls._client[path] = client
        return cls._client[path]

    @classmethod
    def from_disk(cls, collection: str):
        client = cls.get_client(path=str(cfg.db_dir))
        collections = client._client.collections.keys()
        if not (collection in collections):
            client.recreate_collection(
                **{'collection_name': collection,
                   'vectors_config': VectorParams(
                       size=1536, distance=Distance.COSINE, hnsw_config=None, quantization_config=None, on_disk=True
                   ),
                   'shard_number': None,
                   'replication_factor': None,
                   'write_consistency_factor': None,
                   'on_disk_payload': None,
                   'hnsw_config': None,
                   'optimizers_config': None,
                   'wal_config': None, 'quantization_config': None,
                   'init_from': None, 'timeout': None}
            )
        qdrant = cls(
            client=client,
            collection_name=collection,
            embeddings=llm.embedding,
        )

        return qdrant

    @classmethod
    def from_memory(cls, collection: str):
        qdrant = cls(
            client=cls.get_client(":memory:"),
            collection_name=collection,
            embeddings=llm.embedding,
        )
        return qdrant