import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import fs from "node:fs";
import path from "node:path";

export default function (pi: ExtensionAPI) {
  let searchAlreadyCalled = false;

  pi.on("before_agent_start", async (event) => {
    return {
      systemPrompt: `${event.systemPrompt}

## Lenny Growth Assistant

You answer questions using Lenny's podcast and newsletter content.

STRICT RULES:

1. For every factual question about Lenny's content, call search_lenny FIRST.

2. You MUST call search_lenny exactly once.

3. The search_lenny query MUST be exactly the query supplied by the application.

4. Do NOT rewrite, summarize, simplify, expand, or transform the search query.

5. The content returned by search_lenny is the ONLY factual evidence you may use.

6. Do NOT use your own knowledge or outside knowledge.

7. The content field of the results returned by search_lenny
   contains the relevant transcript excerpts. Treat those excerpts
   as authoritative evidence.

8. Every factual claim in your answer must be directly supported by
   the retrieved transcript content.

9. If the retrieved content directly discusses the person, topic,
   recommendation, or question being asked, use that content to
   answer the question.

10. Do NOT say there is insufficient information merely because the
    exact wording of the user's question does not appear in the
    transcript.

11. When an idea comes from a guest, clearly attribute it to that guest.

12. If the retrieved content genuinely does not contain enough
    information to answer the question, respond exactly:

"The provided Lenny content does not contain enough information to answer this."

13. Keep the answer concise and answer the CURRENT question directly.

IMPORTANT:
Search first.
Use the application's exact search query.
Then answer only from the returned Lenny content.
`,
    };
  });

  pi.registerTool({
    name: "search_lenny",
    label: "Search Lenny",

    description:
      "Search Lenny's podcast and newsletter knowledge base. " +
      "The application-provided query is authoritative and must be used exactly.",

    parameters: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description:
            "Query for Lenny search. This value is ignored when " +
            "LENNY_SEARCH_QUERY is provided by the application.",
        },
        limit: {
          type: "number",
          description: "Maximum number of results to return.",
          default: 5,
        },
      },
      required: ["query"],
    },

    async execute(_toolCallId, params) {
      if (searchAlreadyCalled) {
        throw new Error("search_lenny can only be called once");
      }

      searchAlreadyCalled = true;

      /*
       * The Python application provides the authoritative query
       * through LENNY_SEARCH_QUERY.
       *
       * The model's query is intentionally NOT trusted.
       */
      const applicationQuery = process.env.LENNY_SEARCH_QUERY;

      if (!applicationQuery) {
        throw new Error("LENNY_SEARCH_QUERY is missing");
      }

      const query = applicationQuery;

      const searchLimit = Number(
        process.env.LENNY_SEARCH_LIMIT ?? params.limit ?? 5
      );

      console.error("=== SEARCH_Lenny CALLED ===");
      console.error("MODEL QUERY:", params.query);
      console.error("APPLICATION QUERY:", applicationQuery);
      console.error("QUERY USED:", query);
      console.error("LIMIT:", searchLimit);

      const response = await fetch(
        "http://127.0.0.1:8000/agent/search",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query,
            limit: searchLimit,
          }),
        }
      );

      if (!response.ok) {
        const error = await response.text();

        throw new Error(
          `Lenny search failed (${response.status}): ${error}`
        );
      }

      const results = await response.json();

      const resultsPath = path.join(
        process.cwd(),
        ".pi",
        "lenny-search-results.json"
      );

      fs.writeFileSync(
        resultsPath,
        JSON.stringify(results, null, 2),
        "utf-8"
      );

      console.error("HTTP STATUS:", response.status);

      console.error(
        "SEARCH RESULTS:",
        JSON.stringify(results, null, 2)
      );

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(results, null, 2),
          },
        ],
      };
    },
  });
}