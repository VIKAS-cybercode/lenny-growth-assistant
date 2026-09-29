from llm.provider import generate_with_provider


def rewrite_query(
    question: str,
    history: str = "",
) -> str:

    if not history.strip():
        return question.strip()

    prompt = f"""
Rewrite the current question into a standalone search query.

IMPORTANT:
The conversation history is authoritative.

When resolving a follow-up question:
- Preserve the exact person mentioned in the conversation.
- Preserve the exact topic mentioned in the conversation.
- Resolve "he", "she", "they", "this", "that", "it".
- Never replace the person with "Lenny" unless the conversation
  explicitly refers to Lenny.
- Never change the subject of the conversation.
- Do not answer the question.
- Do not add information.
- Return ONLY the rewritten query.

Example:

HISTORY:
USER: How does Adam Ward describe talent density?
ASSISTANT: Adam Ward describes talent density as a collective property
of individuals and teams.

QUESTION:
What does he recommend?

OUTPUT:
What does Adam Ward recommend for building high talent density teams?

--------------------------------------------------
HISTORY
--------------------------------------------------

{history}

--------------------------------------------------
CURRENT QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
OUTPUT
--------------------------------------------------
"""

    return generate_with_provider(prompt).strip()