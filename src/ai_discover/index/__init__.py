from langchain.vectorstores.qdrant import Qdrant, VectorStore

from index.vector import VTS, split_text


vts: VectorStore = VTS.from_disk('ai_discover')