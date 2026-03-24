import os
import faiss

from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document

from app.utils.embedding_utils import embeddings_client
from app.config.env_config import settings
from app.config.log_config import logger

from typing import List, Optional

class FaissVectorStore:
  """Handles embedding storage and retrieval using FAISS."""

  def __init__(self):
    self.index_path = os.path.join(settings.WORKING_PROJECT_DIR, "faiss_index")

    if os.path.exists(self.index_path):
      logger.info(f"Loading existing FAISS index from {self.index_path}")
      self.vector_store = FAISS.load_local(
        self.index_path, 
        embeddings_client, 
        allow_dangerous_deserialization=True
      )
    else:
      logger.info("Initializing new FAISS index")
      self.index = faiss.IndexFlatL2(
        len(embeddings_client.embed_query("Hello World"))
      )
      self.vector_store = FAISS(
        embedding_function=embeddings_client,
        index=self.index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
      )

  def add_documents(self, documents: List[Document]):
    """Adds a list of LangChain Document objects to the vector store.
    
    Args:
      documents:
        list of documents processed by RecursiveCharacterSplitter
    """

    if not documents:
      logger.warning("No documents provided to add.")
      return
    
    try:
      self.vector_store.add_documents(documents)
      logger.info(f"Successfully added {len(documents)} documents to FAISS.")
    except Exception as e:
      logger.error(f"Failed to add documents to FAISS: {e}")
      raise

  def similarity_search(self, query: str, k: int = 4) -> List[Document]:
    """Performs a similarity search and returns the top k documents.

    Args:
      query: user query 
      k: select top elements

    Returns:
      List of documents
    """
    try:
      result = self.vector_store.similarity_search(
        query= query,
        k= k
      )

    except Exception as e:
      logger.error(f"FAISS search failed: {e}")
      return []