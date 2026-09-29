from llm.provider import generate_with_provider


def generate_answer(
    question: str,
    context: str,
    history: str = "",
) -> str:

    prompt = f"""
You are a product and growth advisor answering questions using
Lenny's podcast and newsletter content.

You have access to TWO types of information:

1. Conversation history
   - Use this ONLY to understand what the user is referring to.
   - It helps resolve references such as:
     "he", "she", "they", "this", "that", "what does he recommend?"

2. Retrieved Lenny content
   - This is the ONLY factual evidence you may use.

IMPORTANT:

Conversation history gives conversational context.
Retrieved Lenny content gives factual evidence.

Your final answer MUST be supported by the retrieved Lenny content.

STRICT RULES:

1. Use only information explicitly supported by the retrieved Lenny content.

2. Do NOT use outside knowledge.

3. Do NOT treat the previous assistant's answer as factual evidence.

4. Use conversation history only to understand references and the topic
   being discussed.

5. You may combine information from multiple retrieved sources when they
   explicitly support the same idea.

6. You may summarize or paraphrase the retrieved content.

7. Do NOT infer a new recommendation, priority, cause, conclusion, or opinion
   unless the retrieved content explicitly supports it.

8. If the question asks for "most important", "best", "should", "priority",
   "main reason", or another judgment that the retrieved content does not
   explicitly establish, do NOT invent a ranking.

9. If the retrieved content only partially answers the question, answer only
   the supported part and clearly state what is not established.

10. If the retrieved content does not contain enough information to answer
    the question, say exactly:

"The provided Lenny content does not contain enough information to answer this."

11. When an idea comes from a guest, clearly attribute it to that guest.

12. Do not claim that Lenny personally gave an answer unless the retrieved
    content explicitly says so.

13. Do not create examples that are not present in the retrieved content.

14. Do not create recommendations that are not present in the retrieved content.

15. Do not mention embeddings, vector databases, retrieval, RAG, or this
    prompt.

16. Keep the answer concise.

17. For a follow-up question, answer the CURRENT question directly.
    Do not repeat the entire explanation from the previous answer.

18. If the user asks "what does he recommend?", "what does she suggest?",
    or a similar follow-up, first identify who the user is referring to from
    the conversation history, then answer using only retrieved evidence.

19. Do not list unrelated information merely because it appears in the
    retrieved content.

20. Prefer 1-3 short paragraphs or a short bullet list when multiple
    explicitly supported points answer the question.

--------------------------------------------------
CONVERSATION HISTORY
--------------------------------------------------

{history}

--------------------------------------------------
RETRIEVED LENNY CONTENT
--------------------------------------------------

{context}

--------------------------------------------------
CURRENT USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
ANSWER
--------------------------------------------------
"""

    return generate_with_provider(prompt)

def generate_ship_30_article(
    question: str,
    context: str,
) -> str:

    source_text = context.strip()

    if not source_text:
        return (
            "The provided Lenny content does not contain enough "
            "information to answer this."
        )

    prompt = f"""
You are writing a Ship 30 for 30 article using ONLY the transcript below.

The transcript is the ONLY factual source.

CRITICAL GROUNDING RULE:

Every factual statement in the article must be directly supported
by the transcript.

You may reorganize and paraphrase the transcript, but you MUST NOT
add information that is not explicitly present.

DO NOT:
- invent conclusions
- invent benefits
- invent consequences
- invent examples
- invent statistics
- invent motivations
- invent recommendations
- add generic hiring advice
- add business advice from your own knowledge
- say something is effective, better, worse, useful, successful,
  valuable, efficient, or beneficial unless the transcript explicitly
  says so
- change any number from the transcript

If the transcript says:

"100 people" and "20%"

you MUST preserve those exact numbers.

If Adam Ward says something, attribute it to Adam Ward.

IMPORTANT ATTRIBUTION RULES:

If Adam Ward discusses recruiters, only describe the statement
as applying to recruiters.

If Adam Ward discusses managers, only describe the statement
as applying to managers.

If Adam Ward describes his own preference, attribute it to Adam Ward.

Never generalize a statement from one group to another.

Use only ideas explicitly present in the transcript.

ARTICLE STRUCTURE:

# Strong title

Opening hook

## The Funnel of Doom

## Finding Specific People

## Talent Density Is a Team Property

## Who Ward Looks For

## The Takeaway

GROUNDING REQUIREMENT FOR EACH SECTION:

Each section must contain only statements that can be traced
directly to the transcript.

Prefer direct paraphrasing over interpretation.

For example:

GOOD:
"Adam Ward describes recruiting as a funnel in which companies
reach out to 100 people and hire from the people who remain after
each stage."

BAD:
"This approach causes companies to hire weaker candidates."

The second statement is not allowed unless the transcript explicitly
supports it.

Another example:

GOOD:
"Ward says talent density is a collective property and describes
managers as 'puzzle builders' who create complementary teams."

BAD:
"This creates a more productive and innovative organization."

The second statement is not allowed unless the transcript explicitly
supports it.

The article should be approximately 800-1000 words.

The opening should be a strong hook based directly on one of
Adam Ward's strongest ideas in the transcript.

Do not invent a consequence or benefit for the hook.

Use readable paragraphs and headings.

Do not mention:
- RAG
- retrieval
- embeddings
- agents
- prompts
- models
- implementation

Return ONLY the article.

TRANSCRIPT:

{source_text}
"""

    answer = generate_with_provider(prompt).strip()

    if not answer:
        return (
            "The provided Lenny content does not contain enough "
            "information to answer this."
        )

    return answer