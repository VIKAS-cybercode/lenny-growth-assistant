import sys
from pathlib import Path

# Add backend/ to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer
from sqlalchemy import select

from database import SessionLocal
from models.document_chunk import DocumentChunk


embedding_model = SentenceTransformer(
    "BAAI/bge-large-en-v1.5"
)


def search(query: str, limit: int = 5):
    # Convert user's question into a vector
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    db = SessionLocal()

    try:
        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        )

        statement = (
            select(DocumentChunk, distance.label("distance"))
            .order_by(distance)
            .limit(limit)
        )

        results = db.execute(statement).all()

        print("\n" + "=" * 80)
        print("RAG SEARCH")
        print("Query:", query)
        print("Number of results:", len(results))

        for i, (chunk, distance_value) in enumerate(
            results,
            start=1,
        ):
            print("\n" + "-" * 80)
            print(f"Result {i}")
            print(f"Distance: {distance_value:.4f}")
            print(f"Title: {chunk.title}")
            print(
                f"Source: "
                f"{chunk.source_type}/{chunk.source_id}"
            )
            print(f"Chunk: {chunk.chunk_index}")
            print("Content:")
            print(chunk.content[:500])

        print("=" * 80 + "\n")

        return results

    finally:
        db.close()


def main():
    query = "How do you build high talent density teams?"

    print(f"Query: {query}")
    print("\nTop results:\n")

    results = search(query)

    for i, (chunk, distance) in enumerate(results, start=1):
        print("=" * 80)
        print(f"Result {i}")
        print(f"Distance: {distance:.4f}")
        print(f"Title: {chunk.title}")
        print(f"Source: {chunk.source_type}/{chunk.source_id}")
        print(f"Chunk: {chunk.chunk_index}")
        print()
        print(chunk.content[:1000])
        print()


if __name__ == "__main__":
    main()