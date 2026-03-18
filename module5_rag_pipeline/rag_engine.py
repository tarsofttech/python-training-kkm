"""
RAG Engine - Complete RAG Pipeline with FAISS Vector Store

This module provides a RAGEngine class that handles:
- Building FAISS vector indices from documents
- Persisting and loading indices
- Querying with retrieval-augmented generation
- Source attribution and confidence scoring
"""

from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.core.schema import TextNode
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.faiss import FaissVectorStore
from typing import List, Optional
import faiss
import os


class RAGEngine:
    """
    Complete RAG engine with FAISS vector store.
    
    This class manages the entire RAG pipeline:
    - Document embedding and indexing
    - Persistent storage
    - Semantic search and retrieval
    - Answer generation with source attribution
    """
    
    def __init__(
        self,
        ollama_base_url: str = "http://localhost:11434",
        model: str = "llama3.1",
        embed_model: str = "nomic-embed-text",
        index_path: str = "./data/index",
        embed_dim: int = 768
    ):
        """
        Initialize the RAG engine.
        
        Args:
            ollama_base_url: Base URL for Ollama service
            model: LLM model name for generation
            embed_model: Embedding model name
            index_path: Path to store/load the FAISS index
            embed_dim: Dimension of embedding vectors (768 for nomic-embed-text)
        """
        self.ollama_base_url = ollama_base_url
        self.model_name = model
        self.embed_model_name = embed_model
        self.index_path = index_path
        self.embed_dim = embed_dim
        
        self.llm = Ollama(
            model=model,
            base_url=ollama_base_url,
            request_timeout=120.0
        )
        
        self.embed_model = OllamaEmbedding(
            model_name=embed_model,
            base_url=ollama_base_url
        )
        
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        
        self.index: Optional[VectorStoreIndex] = None
        self.vector_store: Optional[FaissVectorStore] = None
        
        print(f"🤖 RAG Engine initialized")
        print(f"   LLM: {model}")
        print(f"   Embeddings: {embed_model}")
        print(f"   Index path: {index_path}")
    
    async def build_index(self, nodes: List[TextNode]) -> None:
        """
        Build a FAISS index from text nodes and persist to disk.
        
        This creates a new index, embeds all nodes, and saves the index
        for future use.
        
        Args:
            nodes: List of TextNode objects to index
        """
        if not nodes:
            raise ValueError("Cannot build index from empty node list")
        
        print(f"🔨 Building FAISS index from {len(nodes)} nodes...")
        
        faiss_index = faiss.IndexFlatL2(self.embed_dim)
        
        self.vector_store = FaissVectorStore(faiss_index=faiss_index)
        
        storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        
        self.index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            show_progress=True
        )
        
        os.makedirs(self.index_path, exist_ok=True)
        
        self.vector_store.persist(persist_path=os.path.join(self.index_path, "vector_store.json"))
        self.index.storage_context.persist(persist_dir=self.index_path)
        
        print(f"✅ Index built and persisted to {self.index_path}")
        print(f"   Total nodes indexed: {len(nodes)}")
    
    async def load_index(self) -> bool:
        """
        Load an existing FAISS index from disk.
        
        Returns:
            bool: True if index was loaded successfully, False otherwise
        """
        if not os.path.exists(self.index_path):
            print(f"⚠️  Index path does not exist: {self.index_path}")
            return False
        
        vector_store_path = os.path.join(self.index_path, "vector_store.json")
        
        if not os.path.exists(vector_store_path):
            print(f"⚠️  Vector store not found at: {vector_store_path}")
            return False
        
        try:
            print(f"📂 Loading index from {self.index_path}...")
            
            self.vector_store = FaissVectorStore.from_persist_path(vector_store_path)
            
            storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store,
                persist_dir=self.index_path
            )
            
            self.index = VectorStoreIndex.from_vector_store(
                vector_store=self.vector_store,
                storage_context=storage_context
            )
            
            print(f"✅ Index loaded successfully")
            return True
        
        except Exception as e:
            print(f"❌ Error loading index: {e}")
            return False
    
    async def query(
        self,
        question: str,
        top_k: int = 3,
        return_augmented_prompt: bool = False
    ) -> dict:
        """
        Query the RAG system with a question.
        
        This performs semantic search to find relevant chunks,
        then uses the LLM to generate an answer based on the context.
        
        Args:
            question: The user's question
            top_k: Number of relevant chunks to retrieve
            return_augmented_prompt: If True, include the prompt sent to LLM
        
        Returns:
            dict: Contains answer, sources, confidence, and optionally augmented_prompt
        """
        if not self.is_ready():
            raise RuntimeError("Index not loaded. Call load_index() or build_index() first.")
        
        print(f"🔍 Querying: {question}")
        print(f"   Retrieving top {top_k} chunks...")
        
        query_engine = self.index.as_query_engine(
            similarity_top_k=top_k,
            response_mode="compact"
        )
        
        response = query_engine.query(question)
        
        sources = []
        for node in response.source_nodes:
            source_name = node.metadata.get('file_name', 'Unknown')
            score = node.score if hasattr(node, 'score') else 0.0
            sources.append(f"{source_name} (score: {score:.2f})")
        
        avg_score = sum(
            node.score for node in response.source_nodes if hasattr(node, 'score')
        ) / len(response.source_nodes) if response.source_nodes else 0.0
        
        result = {
            "answer": str(response),
            "sources": sources,
            "node_count": len(response.source_nodes),
            "confidence": round(avg_score, 2)
        }
        
        if return_augmented_prompt:
            context_str = "\n\n".join([
                f"[Source: {node.metadata.get('file_name', 'Unknown')}]\n{node.text}"
                for node in response.source_nodes
            ])
            
            augmented_prompt = f"""Context information from relevant documents:

{context_str}

Based on the context above, please answer the following question:
Question: {question}

Answer:"""
            
            result["augmented_prompt"] = augmented_prompt
        
        print(f"✅ Query complete")
        print(f"   Retrieved {len(response.source_nodes)} chunks")
        print(f"   Confidence: {avg_score:.2f}")
        
        return result
    
    def is_ready(self) -> bool:
        """
        Check if the RAG engine is ready to handle queries.
        
        Returns:
            bool: True if index is loaded, False otherwise
        """
        return self.index is not None
    
    def get_node_count(self) -> int:
        """
        Get the total number of nodes in the index.
        
        Returns:
            int: Number of indexed nodes, or 0 if index not loaded
        """
        if not self.is_ready():
            return 0
        
        return len(self.index.docstore.docs)
