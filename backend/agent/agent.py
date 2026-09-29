import json
import os
import subprocess

from dotenv import load_dotenv

from rag.generate import (
    generate_answer,
    generate_ship_30_article,
)


load_dotenv()


def run_agent(
    question: str,
    search_query: str,
    history: str = "",
) -> dict:

    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    extension_path = os.path.join(
        project_root,
        ".pi",
        "extensions",
        "lenny-search.ts",
    )

    # --------------------------------------------------------
    # Detect Ship 30 mode
    # --------------------------------------------------------

    is_ship_30 = any(
        phrase in question.lower()
        for phrase in [
            "ship 30 for 30",
            "ship 30",
            "30 for 30",
        ]
    )

    # Ship 30 needs more transcript context.
    # Normal questions continue using 5 results.
    search_limit = 10 if is_ship_30 else 5

    # --------------------------------------------------------
    # Prompt for Pi
    # --------------------------------------------------------

    prompt = (
        "You MUST call search_lenny exactly once.\n"
        f"Use this exact query: {search_query}\n"
        f"Retrieve the relevant Lenny content for this question: {question}\n"
        "Do not answer the question yourself.\n"
        "After calling search_lenny, stop."
    )

    # --------------------------------------------------------
    # Pi provider/model configuration
    # --------------------------------------------------------

    provider = os.getenv(
        "MODEL_PROVIDER",
        "ollama",
    ).lower()

    if provider == "ollama":
        model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.2:3b",
        )
    elif provider == "openai":
        model = os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini",
        )
    else:
        raise ValueError(
            f"Unsupported MODEL_PROVIDER for Pi: {provider}"
        )

    # --------------------------------------------------------
    # Ship 30 skill
    # --------------------------------------------------------

    skill_path = os.path.join(
        project_root,
        ".pi",
        "skills",
        "ship-30-for-30",
    )

    command = [
        r"C:\Users\Dell\AppData\Roaming\npm\pi.cmd",
        "--provider",
        provider,
        "--model",
        model,
        "--no-builtin-tools",
        "-e",
        extension_path,
        "--skill",
        skill_path,
        "--print",
        prompt,
    ]

    # --------------------------------------------------------
    # Environment for Pi extension
    # --------------------------------------------------------

    env = os.environ.copy()

    env["LENNY_SEARCH_QUERY"] = search_query
    env["LENNY_SEARCH_LIMIT"] = str(search_limit)

    # --------------------------------------------------------
    # Debug logging
    # --------------------------------------------------------

    print("\n--- COMMAND ---")
    print(command)

    print("\n--- CWD ---")
    print(project_root)

    print("\n--- EXTENSION ---")
    print(extension_path)

    print("\n--- EXISTS ---")
    print(os.path.exists(extension_path))

    print("\n--- MODEL PROVIDER ---")
    print(provider)

    print("\n--- MODEL ---")
    print(model)

    print("\n--- LENNY_SEARCH_QUERY ---")
    print(search_query)

    print("\n--- LENNY_SEARCH_LIMIT ---")
    print(search_limit)

    # --------------------------------------------------------
    # Run Pi
    # --------------------------------------------------------

    process = subprocess.run(
        command,
        cwd=project_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    print("\n--- STDOUT ---")
    print(process.stdout)

    print("\n--- STDERR ---")
    print(process.stderr)

    print("\n--- RETURN CODE ---")
    print(process.returncode)

    if process.returncode != 0:
        raise RuntimeError(process.stderr)

    # --------------------------------------------------------
    # Read search results created by search_lenny
    # --------------------------------------------------------

    results_path = os.path.join(
        project_root,
        ".pi",
        "lenny-search-results.json",
    )

    if not os.path.exists(results_path):
        raise RuntimeError(
            "search_lenny did not create lenny-search-results.json"
        )

    try:
        with open(
            results_path,
            "r",
            encoding="utf-8",
        ) as file:
            sources = json.load(file)

    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Could not read search results: {exc}"
        ) from exc

    # --------------------------------------------------------
    # Generate grounded answer
    # --------------------------------------------------------

    if not sources:

        answer = (
            "The provided Lenny content does not contain enough "
            "information to answer this."
        )

    else:

        context_parts = []

        generation_sources = [
            source
            for source in sources
            if source.get("source") == sources[0].get("source")
        ][:6]

        for item in generation_sources:
            context_parts.append(
                f"Title: {item.get('title', '')}\n"
                f"Source: {item.get('source', '')}\n"
                f"Chunk: {item.get('chunk', '')}\n"
                f"Content:\n{item.get('content', '')}"
            )

        context = "\n\n---\n\n".join(context_parts)

        if is_ship_30:

            answer = generate_ship_30_article(
                question=question,
                context=context,
            )

        else:

            answer = generate_answer(
                question=question,
                context=context,
                history=history,
            )

    artifact = None

    if is_ship_30:
        artifact = {
            "type": "markdown",
            "title": "Ship 30 for 30",
            "content": answer,
        }

    return {
        "answer": answer,
        "sources": sources,
        "artifact": artifact,
    }