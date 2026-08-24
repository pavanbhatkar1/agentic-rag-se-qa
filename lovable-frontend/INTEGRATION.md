# Lovable frontend integrated with FastAPI

This frontend now calls the real FastAPI backend at `POST /query` instead of the original simulated pipeline.

Local development:
1. Start the backend on port 10000:
   `uvicorn app.main:app --reload --host 0.0.0.0 --port 10000`
2. In this frontend folder:
   `npm install`
3. Start the Lovable UI:
   `npm run dev`
4. Open the URL printed by Vite (usually `http://localhost:5173`).

The Vite dev server proxies `/query` to `http://localhost:10000`, so no CORS change is required for local development.

Production/build:
`npm run build`

The Vite build output is configured to go to the repository's root `frontend/` directory so FastAPI can serve the compiled `index.html` from `/app`.
