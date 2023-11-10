from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

chatGPT = ChatOpenAI(model="gpt-3.5-turbo",  temperature=0.7)
chatGPT0613 = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)
embedding = OpenAIEmbeddings(model="text-embedding-ada-002")