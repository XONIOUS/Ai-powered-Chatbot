# DocChat — Talk to your PDF

A Flask app that lets you upload any PDF and chat with it using GPT-4o mini + FAISS vector search. Uploads and indexes are stored permanently on Cloudflare R2.

## Features
- Upload any PDF and ask questions about it
- Answers sourced strictly from the document
- Persistent storage via Cloudflare R2
- Clean, dark-mode chat UI

## Project Structure
```
pdf-chatbot/
├── app.py              # Flask routes
├── chatbot.py          # LLM answer generation
├── vector_store.py     # FAISS index creation
├── pdf_loader.py       # PDF text extraction
├── r2_storage.py       # Cloudflare R2 upload/download
├── requirements.txt
├── render.yaml         # Render deployment config
├── .env.example        # Environment variable template
└── templates/
    └── index.html      # Frontend UI
```

## Local Setup

1. Clone the repo
```bash
git clone https://github.com/yourname/pdf-chatbot.git
cd pdf-chatbot
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

5. Run the app
```bash
python app.py
```

6. Open in browser: http://localhost:5000

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `CF_ACCOUNT_ID` | Cloudflare Account ID |
| `CF_ACCESS_KEY_ID` | R2 Access Key ID |
| `CF_SECRET_ACCESS_KEY` | R2 Secret Access Key |
| `CF_BUCKET_NAME` | R2 Bucket name (e.g. `pdf-chatbot`) |
| `FLASK_DEBUG` | Set to `true` only in development |

## Deploy to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Add all environment variables in the Render dashboard
5. Deploy — Render uses `render.yaml` automatically

## Tech Stack
- **Backend:** Flask, LangChain, FAISS, OpenAI
- **Storage:** Cloudflare R2 (S3-compatible)
- **Frontend:** Vanilla HTML/CSS/JS
- **Deploy:** Render
