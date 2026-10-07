# Context Engine V1

A small, working FastAPI service that builds a context JSON object from a sample user profile and the client's goal and task. Memories and documents are empty in V1. The collector is the boundary where later versions can replace sample data with database, memory, and document retrieval.

## Requirements

- Windows
- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/)

Only FastAPI, Pydantic, Uvicorn, and python-dotenv are direct Python dependencies. No database, LLM, retrieval, or agent framework is used.

## Set up with uv (PowerShell)

Open PowerShell in this `context-engine` folder, then run:

```powershell
uv venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

`uv venv` creates an isolated Python environment in `.venv`. The second command installs the four listed packages into that environment.

## Run the API

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` to explore and call the endpoint in FastAPI's interactive API page.

## Verify `POST /context/build`

In a second PowerShell window, from this folder, run:

```powershell
$body = @{
  user_id = "user_001"
  goal = "Get an AI internship"
  task = "Find suitable AI/ML internships"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/context/build `
  -ContentType "application/json" `
  -Body $body | ConvertTo-Json -Depth 5
```

The result should contain the sample Subhasish profile, the same goal and task, and empty `memories` and `documents` arrays. Invalid or missing required fields receive FastAPI's standard HTTP 422 validation response.

## How the pieces fit together

1. `app/main.py` creates the FastAPI application and loads `.env`.
2. `app/api/routes.py` defines `POST /context/build` and validates the incoming request through Pydantic.
3. `app/context/engine.py` coordinates the flow: collect data, then ask the builder to assemble it.
4. `app/context/collector.py` is the V1 data-source boundary. It returns a sample profile and empty memory/document lists.
5. `app/context/builder.py` creates the final response model.
6. `app/context/schema.py` defines the request and response contracts.

This separation keeps the API stable when V2 replaces the hardcoded collector with persistent profile data.
