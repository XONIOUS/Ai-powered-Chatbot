from supabase import create_client
import os

def get_supabase():
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_KEY")
    )

BUCKET = os.getenv("SUPABASE_BUCKET", "pdf-chatbot")

def upload_file_to_r2(local_path, storage_key):
    """Upload a local file to Supabase Storage."""
    supabase = get_supabase()
    with open(local_path, "rb") as f:
        data = f.read()
    supabase.storage.from_(BUCKET).upload(
        path=storage_key,
        file=data,
        file_options={"upsert": "true"}
    )
    print(f"Uploaded {local_path} to Supabase as {storage_key}")

def download_file_from_r2(storage_key, local_path):
    """Download a file from Supabase Storage to local path."""
    supabase = get_supabase()
    data = supabase.storage.from_(BUCKET).download(storage_key)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(data)
    print(f"Downloaded {storage_key} from Supabase to {local_path}")

def file_exists_in_r2(storage_key):
    """Check if a file exists in Supabase Storage."""
    supabase = get_supabase()
    try:
        files = supabase.storage.from_(BUCKET).list(storage_key.rsplit("/", 1)[0])
        filename = storage_key.rsplit("/", 1)[-1]
        return any(f["name"] == filename for f in files)
    except Exception:
        return False
