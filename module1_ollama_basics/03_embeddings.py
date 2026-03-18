"""
Module 1, Script 3: Text Embeddings with Ollama

This script demonstrates how to generate embeddings (vector representations) of text.
Embeddings are numerical representations that capture the semantic meaning of text,
enabling similarity comparisons and semantic search.
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")


def generate_embedding(text: str, model: str = EMBED_MODEL) -> list:
    """
    Generate an embedding vector for the given text.
    
    Args:
        text: The text to embed
        model: The embedding model to use
    
    Returns:
        list: A list of floats representing the embedding vector
    """
    url = f"{OLLAMA_HOST}/api/embeddings"
    
    payload = {
        "model": model,
        "prompt": text,
        "think": True
    }
    
    print(f"📤 Generating embedding for: '{text[:50]}...'")
    
    try:
        response = httpx.post(url, json=payload, timeout=120.0)
        response.raise_for_status()
        return response.json()["embedding"]
    except httpx.ConnectError:
        print("❌ Error: Cannot connect to Ollama. Make sure it's running!")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def calculate_cosine_similarity(vec1: list, vec2: list) -> float:
    """
    Calculate cosine similarity between two vectors.
    Returns a value between -1 and 1, where 1 means identical direction.
    """
    import math
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


def main():
    """Demonstrate text embeddings and similarity comparison."""
    
    print("=" * 80)
    print("🧮 TEXT EMBEDDINGS DEMONSTRATION")
    print("=" * 80)
    print("\n💡 What are embeddings?")
    print("   Embeddings are vector representations (lists of numbers) that capture")
    print("   the semantic meaning of text. Similar texts have similar embeddings.\n")
    
    texts = [
        "The cat sat on the mat.",
        "A feline rested on the rug.",
        "Python is a programming language."
    ]
    
    embeddings = []
    
    for i, text in enumerate(texts, 1):
        print(f"\n📝 Text {i}: {text}")
        embedding = generate_embedding(text)
        
        if embedding:
            embeddings.append(embedding)
            print(f"   ✅ Embedding generated!")
            print(f"   📊 Dimension: {len(embedding)} values")
            print(f"   🔢 First 10 values: {embedding[:10]}")
            print(f"   📈 Min value: {min(embedding):.4f}")
            print(f"   📈 Max value: {max(embedding):.4f}")
        else:
            print("   ❌ Failed to generate embedding")
            return
    
    if len(embeddings) == 3:
        print("\n" + "=" * 80)
        print("🔍 SIMILARITY COMPARISON")
        print("=" * 80)
        
        sim_1_2 = calculate_cosine_similarity(embeddings[0], embeddings[1])
        sim_1_3 = calculate_cosine_similarity(embeddings[0], embeddings[2])
        sim_2_3 = calculate_cosine_similarity(embeddings[1], embeddings[2])
        
        print(f"\n📊 Cosine Similarity Scores (0 to 1, higher = more similar):")
        print(f"   • Text 1 ↔ Text 2: {sim_1_2:.4f}")
        print(f"     '{texts[0]}' vs '{texts[1]}'")
        print(f"\n   • Text 1 ↔ Text 3: {sim_1_3:.4f}")
        print(f"     '{texts[0]}' vs '{texts[2]}'")
        print(f"\n   • Text 2 ↔ Text 3: {sim_2_3:.4f}")
        print(f"     '{texts[1]}' vs '{texts[2]}'")
        
        print("\n💡 Notice:")
        print("   • Texts 1 and 2 are semantically similar (cat/feline, mat/rug)")
        print("     so they should have a HIGH similarity score")
        print("   • Text 3 is about programming, completely different topic")
        print("     so it should have LOW similarity with texts 1 and 2")
    
    print("\n" + "=" * 80)
    print("🎯 USE CASES FOR EMBEDDINGS:")
    print("=" * 80)
    print("""
1. Semantic Search:
   Find documents similar to a query, even if they use different words
   
2. Document Clustering:
   Group similar documents together automatically
   
3. Recommendation Systems:
   Recommend items similar to what a user likes
   
4. RAG (Retrieval-Augmented Generation):
   Find relevant context to augment LLM responses (we'll do this in Module 5!)
   
5. Duplicate Detection:
   Find near-duplicate content even with different wording
    """)
    
    print("\n🔬 TODO: Try these experiments:")
    print("   • Add your own text examples and compare their embeddings")
    print("   • Try texts in different languages (if your model supports it)")
    print("   • Compare embeddings of questions and their answers")


if __name__ == "__main__":
    main()
