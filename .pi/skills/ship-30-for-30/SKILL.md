---
name: ship-30-for-30
description: Generate a grounded "Ship 30 for 30" article using Lenny content
---

# Ship 30 for 30

Use this skill when the user asks for a "Ship 30 for 30" article or explicitly asks to turn Lenny's ideas into a Ship 30 for 30 piece.

## Requirements

1. Search Lenny content before writing.
2. Use the existing `search_lenny` tool exactly once.
3. Use the application's provided search query exactly as supplied.
4. Treat the retrieved Lenny content as the only factual evidence.
5. Do not use outside knowledge or invent examples, quotes, people, statistics, or recommendations.
6. Attribute ideas to the relevant guest or source when appropriate.
7. Write approximately 1,250 words.
8. Start with a strong, attention-grabbing hook.
9. Build a clear narrative rather than producing disconnected notes.
10. Use skimmable formatting:
    - descriptive headings
    - short paragraphs
    - bullets or numbered lists where useful
    - bold key ideas where useful
11. End with a practical takeaway the reader can apply.
12. Make the article useful to a product/growth audience.
13. Do not mention RAG, retrieval, embeddings, vector databases, tools, agents, or internal implementation.
14. Do not claim that an idea comes from Lenny unless the retrieved content supports that claim.
15. If the retrieved content does not contain enough information to write a grounded article, say exactly:

"The provided Lenny content does not contain enough information to answer this."

## Structure

Prefer this structure:

# [Strong, specific title]

[Opening hook]

## The core idea

Explain the central idea using the retrieved evidence.

## Why it matters

Explain the implications supported by the retrieved content.

## What the guest recommends

Present the relevant recommendations with attribution.

## How to apply it

Turn the supported ideas into practical steps without adding unsupported claims.

## The takeaway

End with a concise, useful takeaway.

The final article should be approximately 1,250 words and should read like a polished Ship 30 for 30 essay, not a transcript summary.
