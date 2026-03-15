# OpenAI API Connection Test

Simple script to verify OpenAI API connectivity using the API key from the monorepo `.env`.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python test_openai.py
```

Loads `OPENAI_API_KEY` from:
- `capstone_project/backend/.env`
- project root `.env`

## Expected Output

```
Loaded .env from: .../capstone_project/backend/.env
Testing OpenAI API connection...
Response: OK
SUCCESS: OpenAI API connection works.
```
