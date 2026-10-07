
This project builds context for a user's task. V1 introduced the FastAPI context endpoint. V2 moved user profiles into PostgreSQL. V3 adds a basic memory pipeline: it extracts explicit statements from conversation text, saves them for a user, and retrieves relevant memories when building context.

## Version progression

- **V1 — Basic Context Engine:** FastAPI accepts a user ID, goal, and task. The engine, collector, and builder return a context response using a sample profile.
- **V2 — PostgreSQL:** SQLAlchemy stores users, profiles, skills, projects, and preferences. User CRUD endpoints let the API create, read, update, and delete profiles. The context endpoint reads the profile from the database.
- **V3 — Memory:** conversation text is checked for explicit personal statements, saved as user memories, and matched against the goal and task when building context.

Each version extends the same project. V3 keeps the V1 context endpoint and V2 PostgreSQL user data.

## What V3 does

```text
Conversation text
       ↓
Rule-based memory extractor
       ↓
PostgreSQL memory store
       ↓
Keyword retrieval for the current goal and task
       ↓
Context response
```

The extractor recognizes sentences containing cues such as “I want,” “I prefer,” “I have,” “I know,” or “remember that.” It uses simple Python rules, not an LLM. The retriever looks for keyword overlap and returns up to five matching memories. Documents are still empty; document retrieval comes in a later version.

## Project structure

```text
context-engine/
├── app/
│   ├── api/routes.py             # HTTP endpoints
│   ├── context/                  # Context schema, collector, builder, engine
│   ├── database/                 # PostgreSQL connection, tables, user CRUD
│   ├── memory/                   # Memory extraction, storage, retrieval
│   └── main.py                   # Creates the FastAPI application
├── .env.example                  # Database URL template
├── .gitignore                    # Keeps local settings and environment out of Git
├── requirements.txt
└── README.md
```

## Requirements

- Windows and Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/)
- PostgreSQL installed and running

## Set up on Windows

Run PowerShell commands from this `context-engine` folder.

### 1. Create the PostgreSQL database

Create a database named `context_engine` in pgAdmin, or run:

```powershell
createdb -U postgres context_engine
```

The PostgreSQL server must be running. This creates the database; the app creates its tables when it starts.

### 2. Set the database connection

Create your local `.env` file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace `YOUR_POSTGRES_PASSWORD` with the password for your local PostgreSQL user:

```env
APP_NAME=Context Engine V3
DATABASE_URL=postgresql+psycopg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/context_engine
```

Keep `.env` private. It is excluded from Git by `.gitignore`; do not commit or share your database password.

### 3. Install packages with uv

```powershell
uv venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

### 4. Run the API

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to call the API. On startup, SQLAlchemy creates missing tables: `users`, `profiles`, `skills`, `projects`, `preferences`, and `memories`. It does not create the PostgreSQL database itself or migrate changes to existing tables.

## Try the API

Use `/docs` to call these endpoints in order.

### 1. Create a user — `POST /users`

```json
{
  "id": "user_001",
  "name": "Subhasish",
  "education": "B.Tech CS-AIML",
  "skills": ["Python", "Machine Learning", "Deep Learning"],
  "projects": ["RAG Research Paper Assistant"]
}
```

### 2. Extract and save memories — `POST /users/user_001/memories`

```json
{
  "conversation_text": "I want to become an AI Engineer. I prefer remote work. I have experience with Python."
}
```

The response contains the saved memories and their categories (`goal`, `preference`, or `fact`). Repeating a memory for the same user does not save a duplicate. Statements without a recognized cue are ignored.

### 3. List saved memories — `GET /users/user_001/memories`

This returns all memories saved for that user.

### 4. Build context — `POST /context/build`

```json
{
  "user_id": "user_001",
  "goal": "Become an AI Engineer",
  "task": "Find AI Engineer internships"
}
```

The response includes the user profile from PostgreSQL and memories that share keywords with the goal or task. If no memory keywords match, `memories` is an empty list.

## Other user endpoints

- `GET /users/{user_id}` — read a profile.
- `PUT /users/{user_id}` — update only the fields included in the request. Send an empty list to clear skills or projects.
- `DELETE /users/{user_id}` — delete the user and related profile, skills, projects, preferences, and memories.

## How the code is divided

- `app/memory/extractor.py` finds simple, explicit memory statements in text.
- `app/memory/store.py` saves memories and lists them for a user.
- `app/memory/retriever.py` ranks memories by keyword overlap with the current goal and task.
- `app/database/models.py` defines the PostgreSQL tables, including `memories`.
- `app/database/connection.py` loads `.env`, creates the SQLAlchemy engine, and provides request-scoped sessions.
- `app/context/collector.py` reads the user profile and relevant memories.
- `app/context/engine.py` coordinates collection; `app/context/builder.py` assembles the response.
- `app/api/routes.py` exposes user, memory, and context endpoints.

## Common setup errors

- **`DATABASE_URL is missing`** — copy `.env.example` to `.env` and set the PostgreSQL password.
- **`No module named app...`** — run commands from the project root, the folder containing `app`.
- **`No module named psycopg`** — install requirements into this project's virtual environment with the `uv pip install` command above.
- **Connection refused or authentication failed** — check that PostgreSQL is running and that the username, password, port, and database name in `DATABASE_URL` are correct.

V3 is a learning implementation. It uses `Base.metadata.create_all()` to create missing tables. A later production version should use database migrations to manage schema changes.
