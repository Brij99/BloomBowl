# Bloom Bowl Ordering Website

A single-page Flask experience for Bloom Bowl, featuring a futuristic visual system, menu showcase, and an online
order form that feeds directly into the kitchen workflow.

## Features

- **Immersive hero + stats** – custom gradients, a logo mark, and live stats make the brand feel futuristic.
- **Full menu grid** – bowl descriptions and variation prices are rendered from structured data in `app.py`.
- **On-site ordering** – customers can submit orders with their preferred bowl, mood/style, fulfilment mode, boosters,
  and notes. Details are summarised instantly on-screen for the team.
- **Session-safe submissions** – orders are processed on the server and redirected using the
  Post/Redirect/Get pattern to prevent duplicate submissions on refresh.

## Getting Started

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**:
   ```bash
   flask --app app run --debug
   ```

4. Visit `http://127.0.0.1:5000/` in your browser to view the site.

## Project Structure

```text
├─ app.py             # Flask application, menu data, ordering logic
├─ templates/
│  └─ index.html      # Main page template
├─ static/
│  ├─ css/
│  │  └─ style.css    # Futuristic theme styles
│  └─ img/
│     └─ logo-mark.svg
└─ requirements.txt   # Python dependencies
```

## Customization
- Update `MENU`, `SERVING_STYLES`, `EXTRAS`, or `SERVICE_MODES` inside `app.py` to tailor the experience.
- Adjust colours, gradients, or layout in `static/css/style.css`.
- Replace `static/img/logo-mark.svg` with your own vector mark if desired.

## Deployment
Any WSGI-compatible host (Railway, Render, etc.) can run the app. Configure the host to install dependencies from
`requirements.txt` and run `gunicorn app:app` (or an equivalent command) for production.
