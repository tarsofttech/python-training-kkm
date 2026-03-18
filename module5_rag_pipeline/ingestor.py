"""
Document Ingestor - Loading and Chunking Documents with LlamaIndex

This module provides a DocumentIngestor class that handles:
- Loading documents from directories
- Chunking with different strategies (fixed-size, sentence-window)
- Adding metadata to nodes
"""

from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core.node_parser import SentenceSplitter, SentenceWindowNodeParser
from llama_index.core.schema import TextNode
from typing import List
import os


class DocumentIngestor:
    """
    Handles document loading and chunking with LlamaIndex.
    
    This class provides methods for loading documents from directories
    and chunking them using different strategies for optimal retrieval.
    """
    
    def __init__(self):
        """Initialize the DocumentIngestor."""
        pass
    
    def load_documents(self, directory: str) -> List[Document]:
        """
        Load all documents from a directory.
        
        Uses LlamaIndex's SimpleDirectoryReader to load text and PDF files.
        
        Args:
            directory: Path to directory containing documents
        
        Returns:
            List[Document]: List of loaded documents
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        reader = SimpleDirectoryReader(
            input_dir=directory,
            recursive=True
        )
        
        documents = reader.load_data()
        
        print(f"📚 Loaded {len(documents)} document(s) from {directory}")
        
        return documents
    
    def chunk_fixed(
        self,
        documents: List[Document],
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ) -> List[TextNode]:
        """
        Chunk documents using fixed-size chunks with overlap.
        
        Uses SentenceSplitter which tries to respect sentence boundaries
        while maintaining approximately equal chunk sizes.
        
        Args:
            documents: List of documents to chunk
            chunk_size: Target size of each chunk in tokens
            chunk_overlap: Number of overlapping tokens between chunks
        
        Returns:
            List[TextNode]: List of text nodes (chunks)
        """
        splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        nodes = splitter.get_nodes_from_documents(documents)
        
        print(f"✂️  Created {len(nodes)} chunks using fixed-size chunking")
        print(f"   Chunk size: {chunk_size}, Overlap: {chunk_overlap}")
        
        return nodes
    
    def chunk_sentence_window(
        self,
        documents: List[Document],
        window_size: int = 3
    ) -> List[TextNode]:
        """
        Chunk documents using sentence-window approach.
        
        Creates nodes with a window of sentences around each sentence,
        providing more context for each chunk.
        
        Args:
            documents: List of documents to chunk
            window_size: Number of sentences to include in the window
        
        Returns:
            List[TextNode]: List of text nodes with sentence windows
        """
        parser = SentenceWindowNodeParser.from_defaults(
            window_size=window_size,
            window_metadata_key="window",
            original_text_metadata_key="original_text"
        )
        
        nodes = parser.get_nodes_from_documents(documents)
        
        print(f"✂️  Created {len(nodes)} chunks using sentence-window chunking")
        print(f"   Window size: {window_size} sentences")
        
        return nodes
    
    def add_metadata(
        self,
        nodes: List[TextNode],
        metadata: dict
    ) -> List[TextNode]:
        """
        Add custom metadata to all nodes.
        
        Metadata can be used for filtering during retrieval.
        
        Args:
            nodes: List of nodes to add metadata to
            metadata: Dictionary of metadata key-value pairs
        
        Returns:
            List[TextNode]: Nodes with added metadata
        """
        for node in nodes:
            for key, value in metadata.items():
                node.metadata[key] = value
        
        print(f"🏷️  Added metadata to {len(nodes)} nodes: {metadata}")
        
        return nodes


def main():
    """
    Main function to demonstrate and compare chunking strategies.
    
    This loads the sample policy documents and compares different
    chunking methods, printing a comparison table.
    """
    print("=" * 80)
    print("DOCUMENT INGESTION - CHUNKING STRATEGY COMPARISON")
    print("=" * 80)
    
    ingestor = DocumentIngestor()
    
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    if not os.path.exists(data_dir):
        print(f"\n❌ Error: Data directory not found at {data_dir}")
        print("   Please create the data directory and add sample files.")
        return
    
    print(f"\n📂 Loading documents from: {data_dir}\n")
    
    try:
        documents = ingestor.load_documents(data_dir)
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return
    
    if not documents:
        print("❌ No documents found in the data directory")
        return
    
    print(f"\n📄 Documents loaded:")
    for i, doc in enumerate(documents, 1):
        filename = doc.metadata.get('file_name', 'Unknown')
        char_count = len(doc.text)
        print(f"   {i}. {filename} ({char_count} characters)")
    
    print("\n" + "=" * 80)
    print("TESTING CHUNKING STRATEGIES")
    print("=" * 80)
    
    results = []
    
    print("\n1️⃣  Fixed-Size Chunking (512 tokens, 50 overlap)")
    print("-" * 80)
    nodes_fixed_512 = ingestor.chunk_fixed(documents, chunk_size=512, chunk_overlap=50)
    avg_len_512 = sum(len(node.text) for node in nodes_fixed_512) / len(nodes_fixed_512) if nodes_fixed_512 else 0
    results.append(("Fixed (512/50)", 512, len(nodes_fixed_512), int(avg_len_512)))
    
    print("\n2️⃣  Fixed-Size Chunking (256 tokens, 25 overlap)")
    print("-" * 80)
    nodes_fixed_256 = ingestor.chunk_fixed(documents, chunk_size=256, chunk_overlap=25)
    avg_len_256 = sum(len(node.text) for node in nodes_fixed_256) / len(nodes_fixed_256) if nodes_fixed_256 else 0
    results.append(("Fixed (256/25)", 256, len(nodes_fixed_256), int(avg_len_256)))
    
    print("\n3️⃣  Sentence-Window Chunking (window=3)")
    print("-" * 80)
    nodes_window = ingestor.chunk_sentence_window(documents, window_size=3)
    avg_len_window = sum(len(node.text) for node in nodes_window) / len(nodes_window) if nodes_window else 0
    results.append(("Sentence Window (3)", "N/A", len(nodes_window), int(avg_len_window)))
    
    print("\n" + "=" * 80)
    print("COMPARISON TABLE")
    print("=" * 80)
    print(f"\n{'Method':<25} | {'Chunk Size':<12} | {'Node Count':<12} | {'Avg Length':<12}")
    print("-" * 80)
    
    for method, chunk_size, node_count, avg_length in results:
        chunk_size_str = str(chunk_size) if isinstance(chunk_size, int) else chunk_size
        print(f"{method:<25} | {chunk_size_str:<12} | {node_count:<12} | {avg_length:<12}")
    
    print("\n" + "=" * 80)
    print("💡 KEY OBSERVATIONS:")
    print("=" * 80)
    print("""
1. Smaller chunk sizes create more chunks
   • More chunks = more granular retrieval
   • But also more chunks to search through

2. Sentence-window creates variable-sized chunks
   • Better semantic coherence
   • Preserves sentence context
   • May create more chunks than fixed-size

3. Overlap helps maintain context
   • Prevents information loss at chunk boundaries
   • Increases total chunk count slightly
   • Recommended: 10-20% of chunk size
    """)
    
    print("\n🔬 TODO: Try these experiments:")
    print("   • Change chunk_size to 1024 and compare results")
    print("   • Try window_size of 5 for sentence-window chunking")
    print("   • Add metadata and observe how it's preserved in chunks")
    print("   • Load your own documents and compare chunking strategies")
    
    print("\n" + "=" * 80)
    print("✅ Comparison complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
