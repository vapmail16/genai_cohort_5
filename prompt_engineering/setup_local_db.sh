#!/usr/bin/env bash
# Create local PostgreSQL database for prompt_engineering (Technique 6)
# Prerequisite: PostgreSQL running (brew services start postgresql@16)

set -e
echo "Creating database: prompt_demo"
createdb prompt_demo 2>/dev/null && echo "✓ Database created" || echo "Database may already exist"
echo "DATABASE_URL=postgresql://$(whoami)@localhost:5432/prompt_demo"
echo "Add the above to prompt_engineering/.env if not present"
