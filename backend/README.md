# Backend Service

This folder contains the FastAPI backend for the Cloud project.

## Running locally

1. Create a virtual environment and activate it.
2. Install dependencies:
   ```sh
   pip install -r backend/requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your environment variables.
4. Start the server:
   ```sh
   uvicorn backend.server:app --reload
   ```

The API will be available at `http://localhost:8000`.

## Deploying

- A `Procfile` at the project root is provided for Heroku-like platforms:
  ```
  web: uvicorn backend.server:app --host 0.0.0.0 --port $PORT
  ```

- For Render, you can use the following `render.yaml` or configure via the dashboard:
  ```yaml
  services:
    - type: web
      name: backend
      env: python
      plan: free
      buildCommand: pip install -r backend/requirements.txt
      startCommand: python backend/server.py
      repo: https://github.com/Ayak-project/tpaiman
      branch: main
  ```

Ensure the correct environment variables are set on the host (e.g. Supabase and Cloudinary credentials).
