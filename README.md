# Blooomm Bowl Website

A responsive single-page website for Blooomm Bowl built with Python and Flask. The site highlights the brand story and the complete bowl menu, and it is optimized for both mobile and desktop experiences.

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
├─ app.py             # Flask application and menu data
├─ templates/
│  └─ index.html      # Main page template
├─ static/
│  └─ css/
│     └─ style.css    # Custom styles
└─ requirements.txt   # Python dependencies
```

## Customization
- Update `MENU`, `FEATURES`, or contact details in `app.py` to change displayed content.
- Adjust typography, colors, or layout inside `static/css/style.css`.

## Deployment
Any WSGI-compatible host (Railway, Render, etc.) can run the app. Configure the host to install dependencies from `requirements.txt` and run `gunicorn app:app` or an equivalent command.
