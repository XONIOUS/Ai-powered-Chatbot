from flask import Flask, request, jsonify, render_template
import os
from pdf_loader import load_pdf
from langchain_text_splitters import CharacterTextSplitter
from vector_store import create_vector_store
from chatbot import get_answer
from supabase_storage import upload_file_to_r2, download_file_from_r2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
INDEX_FOLDER = "faiss_indexes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INDEX_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def sanitize_name(filename):
    return os.path.splitext(filename)[0].replace(" ", "_")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        upload_file_to_r2(file_path, f"uploads/{file.filename}")

        docs = load_pdf(file_path)
        if not docs:
            return jsonify({"error": "Could not extract text from PDF"}), 400

        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        index_path = os.path.join(INDEX_FOLDER, sanitize_name(file.filename))
        create_vector_store(chunks, index_path)

        for fname in os.listdir(index_path):
            local_file = os.path.join(index_path, fname)
            upload_file_to_r2(local_file, f"indexes/{sanitize_name(file.filename)}/{fname}")

        return jsonify({"message": "PDF uploaded and processed!", "filename": file.filename})

    except Exception as e:
        return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    user_msg = data.get("message", "").strip()
    filename = data.get("filename", "").strip()

    if not user_msg:
        return jsonify({"error": "Message cannot be empty"}), 400
    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    index_name = sanitize_name(filename)
    index_path = os.path.join(INDEX_FOLDER, index_name)

    if not os.path.exists(index_path):
        try:
            os.makedirs(index_path, exist_ok=True)
            for fname in ["index.faiss", "index.pkl"]:
                download_file_from_r2(
                    f"indexes/{index_name}/{fname}",
                    os.path.join(index_path, fname)
                )
        except Exception:
            return jsonify({"error": "PDF index not found. Please upload the PDF first."}), 404

    try:
        reply = get_answer(user_msg, index_path)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": f"Failed to get answer: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
