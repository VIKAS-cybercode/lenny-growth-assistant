from agent.tools import search_lenny


def main():
    results = search_lenny(
        "How does Adam Ward describe talent density?"
    )

    for i, result in enumerate(results, start=1):
        print("=" * 80)
        print(f"Result {i}")
        print("Title:", result["title"])
        print("Source:", result["source"])
        print("Chunk:", result["chunk"])
        print("Distance:", result["distance"])
        print("Content:")
        print(result["content"][:1000])


if __name__ == "__main__":
    main()