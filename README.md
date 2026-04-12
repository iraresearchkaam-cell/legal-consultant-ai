# Legal Consultant AI

Legal Consultant AI is a lightweight Streamlit frontend for a legal research assistant backed by an `n8n` webhook. The UI captures a user's legal question, sends it to the configured backend workflow, and renders the returned answer in a conversational interface.

## Features

- Streamlit chat interface for legal question-and-answer flows
- Configurable backend webhook via environment variable
- Defensive handling for backend failures and malformed JSON responses
- Automated test coverage for the main user journey, backend integration behavior, and edge cases

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── tests/
    ├── conftest.py
    ├── test_app.py
    ├── test_edge_cases.py
    └── test_integration.py
```

## Requirements

- Python 3.9+
- An available `n8n` webhook endpoint for the assistant backend

## Setup

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install runtime dependencies.

```bash
pip install -r requirements.txt
```

3. Install development and test dependencies.

```bash
pip install -r requirements-dev.txt
```

4. Configure the webhook URL.

```bash
cp .env.example .env
export N8N_WEBHOOK_URL="http://localhost:5678/webhook/consultant-bot"
```

## Run the App

```bash
streamlit run app.py
```

The application will open a chat interface titled `AI Legal Consultant`.

## Run Tests

```bash
pytest
```

## Configuration

The application uses the following environment variable:

- `N8N_WEBHOOK_URL`: Overrides the default local webhook endpoint

If the variable is not set, the app falls back to `http://localhost:5678/webhook/consultant-bot`.

## Testing Scope

The automated test suite validates:

- session state initialization and message persistence
- chat history rendering
- successful backend responses
- missing answer fields and malformed JSON handling
- HTTP error reporting
- request exception handling
- end-to-end prompt processing and main app execution
- unicode and whitespace edge cases

## Notes for Production Hardening

Before production deployment, consider:

- adding authentication and rate limiting
- moving secrets and service endpoints into managed environment configuration
- logging backend failures to an observability platform
- introducing structured response validation between Streamlit and `n8n`
