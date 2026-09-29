# Lenny Growth Assistant

An AI-powered conversational growth assistant grounded in Lenny Rachitsky's podcast and newsletter content.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant Lenny content before generating answers. It supports conversational follow-ups, source attribution, a dedicated "Ship 30 for 30" content skill, and Markdown artifact generation.

## Repository

[GitHub Repository](https://github.com/VIKAS-cybercode/lenny-growth-assistant)

---

## Features

- Conversational AI assistant for product and growth questions
- Retrieval-Augmented Generation over Lenny podcast/newsletter content
- PostgreSQL + pgvector for persistent storage and vector search
- `BAAI/bge-large-en-v1.5` embeddings
- Ollama support for local LLM inference
- Optional OpenAI cloud provider
- Provider abstraction through environment configuration
- Independent conversation sessions
- Persistent users, conversations, messages, and sources
- Follow-up question rewriting using conversation history
- Transcript source attribution in responses
- Grounding behavior when retrieved content is insufficient
- Dedicated **Ship 30 for 30** content-generation skill
- Markdown artifact viewer in the frontend
- FastAPI backend
- React + Vite frontend
- Alembic database migrations
- Backend test files for agent and RAG behavior

---

## Demo

The application provides:

- Conversational product and growth Q&A
- Transcript-grounded answers with source information
- Follow-up questions using conversation context
- "Ship 30 for 30" article generation
- Markdown artifact viewing
- Local LLM inference through Ollama
- Persistent conversations

---

## Architecture

```text
                         ┌──────────────────────┐
                         │      React / Vite     │
                         │       Frontend        │
                         └──────────┬───────────┘
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐  ┌────────────────┐  ┌───────────────┐
        │ Conversation   │  │ Agent / Pi      │  │ LLM Provider  │
        │ Persistence    │  │ Integration     │  │ Abstraction   │
        └───────┬────────┘  └───────┬────────┘  └───────┬───────┘
                │                   │                   │
                ▼                   ▼                   ▼
        ┌────────────────┐  ┌────────────────┐  ┌───────────────┐
        │ PostgreSQL +   │  │ Lenny Search   │  │ Ollama /      │
        │ pgvector       │  │ Tool           │  │ OpenAI        │
        └────────────────┘  └───────┬────────┘  └───────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Lenny transcript /   │
                         │ newsletter chunks    │
                         └──────────────────────┘

```

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- Alembic
- Pydantic
- Sentence Transformers
- `BAAI/bge-large-en-v1.5`
- Pi Coding Agent
- Ollama
- OpenAI API (optional)

### Frontend

- React
- Vite
- React Router
- React Markdown
- Remark GFM

---

## Project Structure

```text
lenny-growth-assistant/
│
├── backend/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── tools.py
│   │   ├── test_agent.py
│   │   └── test_tools.py
│   │
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── ingestion/
│   │   └── ingest.py
│   │
│   ├── llm/
│   │   └── provider.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── document_chunk.py
│   │
│   ├── rag/
│   │   ├── generate.py
│   │   ├── query.py
│   │   └── test_rag.py
│   │
│   ├── retrieval/
│   │   └── search.py
│   │
│   ├── routes/
│   │   ├── agent.py
│   │   ├── conversations.py
│   │   └── users.py
│   │
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   ├── Layout.jsx
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
├── .pi/
│   ├── extensions/
│   │   └── lenny-search.ts
│   └── skills/
│       └── ship-30-for-30/
│           └── SKILL.md
│
├── lennys-newsletterpodcastdata/
│   ├── podcasts/
│   ├── newsletters/
│   └── index.json
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Local Setup

### Prerequisites

Install:

- Python 3.11+
- Node.js
- PostgreSQL with pgvector support
- Ollama
- Git
- Pi Coding Agent

The application currently uses PostgreSQL through `DATABASE_URL`.

### 1. Clone the Repository

```bash
git clone https://github.com/VIKAS-cybercode/lenny-growth-assistant.git
cd lenny-growth-assistant
```

### 2. Create the Environment File

Copy the example environment file.

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

Update `.env` with your PostgreSQL connection string.

Example:

```env
DATABASE_URL=your_postgresql_connection_string

MODEL_PROVIDER=ollama

OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2:3b

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

Do not commit `.env`.

### 3. Obtain the Lenny Dataset

The raw Lenny dataset is intentionally not included in this public repository.

The dataset license permits personal, non-commercial use but does not permit redistribution of the raw starter dataset files.

Place the dataset at:

```text
lenny-growth-assistant/
└── lennys-newsletterpodcastdata/
    ├── podcasts/
    ├── newsletters/
    └── index.json
```

The ingestion script expects:

```text
lennys-newsletterpodcastdata/podcasts/
lennys-newsletterpodcastdata/newsletters/
```

If the dataset is not present, ingestion will fail with a clear directory-not-found error.

### 4. Backend Setup

Open a terminal in the project root:

```powershell
cd backend
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### 5. Run Database Migrations

From the backend directory:

```powershell
alembic upgrade head
```

The migration configuration reads `DATABASE_URL` from the environment.

The database contains:

- Users
- Conversations
- Messages
- Document chunks
- Vector embeddings
- Message source metadata

### 6. Ingest the Lenny Content

From the backend directory:

```powershell
python ingestion/ingest.py
```

The ingestion pipeline:

1. Reads podcast and newsletter Markdown files.
2. Parses document metadata.
3. Splits documents into overlapping chunks.
4. Generates embeddings using `BAAI/bge-large-en-v1.5`.
5. Stores chunks and embeddings in PostgreSQL/pgvector.
6. Skips chunks that have already been ingested.

The ingestion process is intentionally separate from application startup.

### 7. Install and Start Ollama

Install Ollama and make sure it is running.

Pull the model configured in `.env`:

```powershell
ollama pull llama3.2:3b
```

Verify:

```powershell
ollama list
```

The application uses:

```env
MODEL_PROVIDER=ollama
```

by default.

The LLM provider can be changed through environment configuration without changing application code.

For example:

```env
MODEL_PROVIDER=openai
```

requires:

```env
OPENAI_API_KEY=your_api_key
```

### 8. Start the Backend

From:

```text
lenny-growth-assistant/backend
```

run:

```powershell
uvicorn main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

Root endpoint:

```text
GET /
```

Expected response:

```json
{
  "message": "Lenny Growth Assistant API is running"
}
```

### 9. Start the Frontend

Open a second terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start Vite:

```powershell
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

### 10. Run the Application

With both services running:

```text
Frontend
http://localhost:5173
        │
        ▼
FastAPI
http://127.0.0.1:8000
        │
        ├── PostgreSQL + pgvector
        ├── Lenny retrieval
        └── Ollama
```

Open:

```text
http://localhost:5173
```

in your browser.

---

## RAG Pipeline

The assistant uses a Retrieval-Augmented Generation pipeline.

```text
User question
      │
      ▼
Conversation history
      │
      ▼
Query rewriting
      │
      ▼
Vector similarity search
      │
      ▼
Relevant Lenny transcript chunks
      │
      ▼
Agent / LLM generation
      │
      ▼
Answer + source metadata
```

Documents are chunked into overlapping sections before embedding.

Embeddings are generated using:

```text
BAAI/bge-large-en-v1.5
```

The resulting 1024-dimensional vectors are stored in PostgreSQL using pgvector.

The retrieval layer performs vector similarity search and returns relevant transcript chunks.

Responses preserve source metadata including:

- Source title
- Source type
- Chunk index

This allows the frontend to display the source information used for an answer.

---

## Conversational Context

Each conversation has its own ID.

Messages are persisted in PostgreSQL:

```text
User
  │
  └── Conversation
        │
        ├── User message
        ├── Assistant message
        ├── User message
        └── Assistant message
```

Follow-up questions use previous conversation messages to rewrite ambiguous questions into standalone retrieval queries.

For example:

```text
User:
How does Adam Ward describe talent density?

Assistant:
...

User:
What does he recommend?
```

The retrieval query is rewritten using the conversation context so that the subject remains Adam Ward rather than being replaced with an unrelated entity.

---

## Agent Integration

The project uses Pi Coding Agent as the agent layer.

The application controls the retrieval query before invoking the agent.

The custom Pi extension provides the Lenny search tool:

```text
.pi/extensions/lenny-search.ts
```

The extension enforces the Lenny-content grounding workflow.

The application also reads the structured retrieval result generated during the agent run rather than trusting free-form agent output for source metadata.

---

## Ship 30 for 30

The project includes a dedicated skill:

```text
.pi/skills/ship-30-for-30/SKILL.md
```

The skill is designed for prompts such as:

```text
Create a Ship 30 for 30 article about hiring.
```

The workflow retrieves relevant Lenny material and generates a structured Markdown article.

The skill specifies:

- Strong opening hook
- Narrative structure
- Skimmable headings
- Practical takeaway
- Attribution to the relevant guest
- Transcript-grounded claims

---

## Artifacts

The assistant can return a generated Markdown artifact.

Artifacts contain:

```text
type
title
content
```

The frontend renders Markdown using:

- React Markdown
- Remark GFM

Artifacts are displayed in a dedicated artifact panel separate from the conversation messages.

Generated content should be treated as untrusted content if HTML rendering is introduced in the future.

---

## API Overview

### Create Anonymous User

```http
POST /users/anonymous
```

Creates an anonymous user and returns a user UUID.

### Create Conversation

```http
POST /conversations
```

Creates a new independent conversation.

### Send Message

```http
POST /conversations/{conversation_id}/messages
```

The endpoint:

1. Validates the conversation.
2. Loads conversation history.
3. Rewrites the retrieval query when necessary.
4. Runs the agent.
5. Retrieves relevant Lenny sources.
6. Generates the response.
7. Persists the assistant message.
8. Returns source metadata and optional artifact data.

### Get Conversations

```http
GET /users/{user_id}/conversations
```

Returns conversations belonging to a user.

### Get Conversation Messages

```http
GET /conversations/{conversation_id}/messages
```

Returns messages for a conversation.

### Agent Search

```http
POST /agent/search
```

Used by the agent layer to retrieve relevant Lenny content.

---

## Project Status

### Implemented

- FastAPI backend
- React frontend
- PostgreSQL persistence
- pgvector retrieval
- Lenny transcript RAG
- Conversational follow-ups
- Pi agent integration
- Ollama provider
- Optional OpenAI provider
- Source attribution
- Ship 30 for 30 skill
- Markdown artifact generation
- Frontend artifact viewer
- Alembic migrations
- Environment-based provider configuration

### In Progress

- HTML artifact isolation/sanitization
- Docker Compose setup
- Final automated test suite
- Final UI polish
- Final documentation and demo packaging

---

## Testing

Backend test files are located in:

```text
backend/agent/test_agent.py
backend/agent/test_tools.py
backend/rag/test_rag.py
```

The automated test suite is still being finalized.

### Frontend Build

```powershell
cd frontend
npm run build
```

### Frontend Lint

```powershell
cd frontend
npm run lint
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `MODEL_PROVIDER` | `ollama` or `openai` |
| `OLLAMA_URL` | Ollama generation endpoint |
| `OLLAMA_MODEL` | Local Ollama model |
| `OPENAI_API_KEY` | Optional OpenAI API key |
| `OPENAI_MODEL` | OpenAI model |

Example:

```env
DATABASE_URL=your_postgresql_connection_string

MODEL_PROVIDER=ollama

OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2:3b

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

---

## Source Data and Licensing

The raw Lenny dataset is not committed to this repository.

The local dataset is used for the assignment's retrieval and grounding workflow.

Users should obtain and use the dataset according to its applicable license terms.

Do not add the raw dataset directory to Git:

```text
lennys-newsletterpodcastdata/
```

The repository `.gitignore` intentionally excludes it.

---

## Security and Secrets

Never commit:

```text
.env
API keys
Database passwords
Private credentials
```

The repository includes:

```text
.env.example
```

as a safe configuration template.

---

## Current Limitations

- The raw Lenny dataset must be supplied separately.
- Ollama must be installed locally for local inference.
- PostgreSQL with pgvector is required for the current RAG setup.
- The current frontend is designed primarily for the local development workflow.
- Artifact rendering currently focuses on Markdown.
- HTML artifacts require additional sanitization and isolation before being rendered as executable HTML.
- Docker Compose setup is not yet included.

---

## Development

### Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### Frontend

```powershell
cd frontend
npm run dev
```

---

## License

This project is an assessment/demo application.

The application's source code and the underlying Lenny content are subject to different rights and should not be treated as having the same license.