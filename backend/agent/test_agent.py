from agent.agent import run_agent
from rag.query import rewrite_query


def main():
    history = """USER: How does Adam Ward describe talent density?
ASSISTANT: Adam Ward describes talent density as a collective property of individuals and teams."""

    question = "What does he recommend?"

    # Resolve "he" before calling the agent.
    search_query = rewrite_query(
        question=question,
        history=history,
    )

    print("\nRewritten query:")
    print(search_query)

    response = run_agent(
        question=question,
        search_query=search_query,
    )

    print("\nAgent response:")
    print(response)


if __name__ == "__main__":
    main()