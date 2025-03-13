"""
Semantic search: Build a semantic search engine over a PDF with document loaders, embedding models, and vector stores.
Reference: https://python.langchain.com/docs/tutorials/retrievers/
"""
import asyncio
from typing import List

from langchain_core.documents import Document
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.runnables import chain

from Hermes_utils.common_utils import CommonUtils

# 0. Load config
config = CommonUtils.get_sys_config()

# 1. Documents and Documents Loaders
# Sample documents
documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

# 1.1 Loading documents
file_path = "nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)
docs = loader.load()
print(len(docs))  # PyPDFLoader loads one Document object per PDF page.
print(type(docs[0]))  # <class 'langchain_core.documents.base.Document'>
print(f"{docs[0].page_content[:200]}")  # page_content
print(docs[0].metadata)
print(docs[0].id)

# 1.2 Splitting
#  We will split our documents into chunks of 1000 characters with 200 characters of overlap between chunks.
#  The overlap helps mitigate the possibility of separating a statement from important context related to it.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
print(len(all_splits))
print(type(all_splits[0]))  # <class 'langchain_core.documents.base.Document'>

# 2. Embeddings
embeddings = OllamaEmbeddings(
    model=config["ollama"]["model"]
)
vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)
assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(f"Generated vectors of type {type(vector_1)}\n")  # list
print(vector_1[:10])

# 3. Vector stores
vector_store = InMemoryVectorStore(
    embedding=embeddings
)
# ids = vector_store.add_documents(documents=all_splits)
ids = vector_store.add_documents(documents=documents)
print(ids)

# 3.1 Usage
# Return documents based on similarity to a string query
results = vector_store.similarity_search(
    "How many distribution centers does Nike have in the US?"
)
print(results[0])


# Async query
async def async_query():
    results = await vector_store.asimilarity_search("When was Nike incorporated?")
    print(results[0])


asyncio.run(async_query())

# Return scores
results = vector_store.similarity_search_with_score("What was Nike's revenue in 2023?")
doc, score = results[0]
print(f"Score: {score}")
print(doc)

# Return documents based on similarity to an embedded query
embedding = embeddings.embed_query("How were Nike's margins impacted in 2023?")
results = vector_store.similarity_search_by_vector(embedding)
print(results[0])


# 4. Retrievers
# Use Runnable
@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)


print(retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
))

# Use as_retriever method
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)
print(retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
))
