import sys
from pathlib import Path

# Add backend/ to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from retrieval.search import search
from rag.generate import generate_answer


def main():
    question = "How do you build high talent density teams?"

    print("Searching Lenny's content...\n")

    results = search(question, limit=3)

    context_parts = []

    for i, (chunk, distance) in enumerate(results, start=1):
        context_parts.append(
            f"""
Source {i}
Title: {chunk.title}
Source: {chunk.source_type}/{chunk.source_id}
Chunk: {chunk.chunk_index}

{chunk.content[:2500]}
"""
        )

    context = "\n".join(context_parts)

    print("Generating answer with Ollama...\n")

    answer = generate_answer(
        question=question,
        context=context,
    )

    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    main()