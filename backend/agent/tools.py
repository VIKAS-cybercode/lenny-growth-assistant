from retrieval.search import search


def search_lenny(query: str, limit: int = 5) -> list[dict]:
    """
    Search Lenny's knowledge base and return relevant sources.
    """

    results = search(query, limit=limit)

    sources = []

    for chunk, distance in results:
        sources.append(
            {
                "title": chunk.title,
                "source": f"{chunk.source_type}/{chunk.source_id}",
                "chunk": chunk.chunk_index,
                "content": chunk.content,
                "distance": float(distance),
            }
        )

    return sources