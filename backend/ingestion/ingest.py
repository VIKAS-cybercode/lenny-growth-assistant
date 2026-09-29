import sys
import uuid
from pathlib import Path

# Add backend/ to Python's import path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import yaml
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import select

from database import SessionLocal
from models.document_chunk import DocumentChunk


load_dotenv()


DATASET_DIR = (
    Path(__file__).resolve().parents[2]
    / "lennys-newsletterpodcastdata"
)

PODCASTS_DIR = DATASET_DIR / "podcasts"
NEWSLETTERS_DIR = DATASET_DIR / "newsletters"


# Local embedding model.
# BGE-large produces 1024-dimensional embeddings.
embedding_model = SentenceTransformer(
    "BAAI/bge-large-en-v1.5"
)


def load_markdown_file(file_path: Path):
    """Read a Markdown file and separate frontmatter from content."""

    text = file_path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        raise ValueError(f"Missing frontmatter: {file_path}")

    parts = text.split("---", 2)

    if len(parts) != 3:
        raise ValueError(f"Invalid frontmatter: {file_path}")

    metadata = yaml.safe_load(parts[1])
    content = parts[2].strip()

    return metadata, content


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
):
    """Split text into overlapping chunks."""

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def get_existing_chunk_indexes(
    db,
    source_id: str,
):
    """Return chunk indexes already stored for a document."""

    statement = select(DocumentChunk.chunk_index).where(
        DocumentChunk.source_id == source_id
    )

    return {
        row[0]
        for row in db.execute(statement).all()
    }


def ingest_file(db, file_path: Path, source_type: str):
    """Ingest one Markdown document."""

    metadata, content = load_markdown_file(file_path)

    source_id = file_path.stem

    chunks = chunk_text(content)

    existing_indexes = get_existing_chunk_indexes(
        db,
        source_id,
    )

    new_chunks = 0
    skipped_chunks = 0

    print()
    print(f"Processing: {file_path.name}")
    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        # Don't generate an embedding if this chunk
        # already exists in PostgreSQL.
        if i in existing_indexes:
            skipped_chunks += 1
            continue

        print(
            f"  Embedding chunk {i + 1}/{len(chunks)}..."
        )

        embedding = embedding_model.encode(
            chunk,
            normalize_embeddings=True,
        ).tolist()

        document_chunk = DocumentChunk(
            id=uuid.uuid4(),
            source_type=source_type,
            source_id=source_id,
            title=metadata["title"],
            content=chunk,
            chunk_index=i,
            embedding=embedding,
        )

        db.add(document_chunk)

        new_chunks += 1

    return new_chunks, skipped_chunks


def main():

    if not PODCASTS_DIR.exists():
        raise RuntimeError(
            f"Podcasts directory not found: {PODCASTS_DIR}"
        )

    if not NEWSLETTERS_DIR.exists():
        raise RuntimeError(
            f"Newsletters directory not found: {NEWSLETTERS_DIR}"
        )

    podcast_files = sorted(
        PODCASTS_DIR.glob("*.md")
    )

    newsletter_files = sorted(
        NEWSLETTERS_DIR.glob("*.md")
    )

    all_files = [
        (file_path, "podcast")
        for file_path in podcast_files
    ] + [
        (file_path, "newsletter")
        for file_path in newsletter_files
    ]

    print("========================================")
    print("Lenny Dataset Ingestion")
    print("========================================")
    print(f"Podcasts: {len(podcast_files)}")
    print(f"Newsletters: {len(newsletter_files)}")
    print(f"Total documents: {len(all_files)}")
    print()

    db = SessionLocal()

    total_new = 0
    total_skipped = 0
    total_failed = 0

    try:

        for file_path, source_type in all_files:

            try:
                new_chunks, skipped_chunks = ingest_file(
                    db,
                    file_path,
                    source_type,
                )

                db.commit()

                total_new += new_chunks
                total_skipped += skipped_chunks

                print(
                    f"  Added: {new_chunks}, "
                    f"Skipped: {skipped_chunks}"
                )

            except Exception as error:

                db.rollback()

                total_failed += 1

                print(
                    f"  ERROR: {file_path.name}"
                )
                print(
                    f"  {error}"
                )

        print()
        print("========================================")
        print("Ingestion complete")
        print("========================================")
        print(f"New chunks:     {total_new}")
        print(f"Skipped chunks: {total_skipped}")
        print(f"Failed files:   {total_failed}")

    finally:
        db.close()


if __name__ == "__main__":
    main()