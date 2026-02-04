#!/usr/bin/env python3
"""
EU AI Act - Gemini File Search Store Setup
==========================================
This script creates a Gemini File Search Store (managed RAG vector database)
and uploads the EU AI Act documents for semantic search capabilities.

Requirements:
    pip install google-genai

Usage:
    export GEMINI_API_KEY="your-api-key-here"
    python setup_ai_act_store.py

After setup, you can query the store using the query_ai_act.py script.
"""

from pathlib import Path
from google import genai
import os

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
STORE_DISPLAY_NAME = "EU-AI-Act-GDPR-Knowledge-Base"
BASE_DIR = Path(__file__).resolve().parent
ARTICLES_DIR = BASE_DIR / "articles"

def create_client():
    """Initialize the Gemini API client."""
    if not GEMINI_API_KEY:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
    return genai.Client(api_key=GEMINI_API_KEY)

def create_file_search_store(client):
    """Create a new File Search Store for the AI Act documents."""
    print(f"Creating File Search Store: {STORE_DISPLAY_NAME}")
    
    # Check if store already exists
    existing_stores = list(client.file_search_stores.list())
    for store in existing_stores:
        if store.display_name == STORE_DISPLAY_NAME:
            print(f"Store already exists: {store.name}")
            return store
    
    # Create new store
    store = client.file_search_stores.create(
        config={'display_name': STORE_DISPLAY_NAME}
    )
    print(f"Created store: {store.name}")
    return store

def iter_article_documents():
    """Yield every file under the articles directory."""
    if not ARTICLES_DIR.exists():
        return []
    return sorted([p for p in ARTICLES_DIR.rglob('*') if p.is_file()])


def get_existing_files(client, store_name):
    """Return a set of display names for files already in the store."""
    print("Checking existing files in store...")
    existing_files = set()
    try:
        # Note: pagination might be needed for >100 files, checking if iterator handles it
        files = client.file_search_stores.documents.list(parent=store_name)
        for f in files:
            if f.display_name:
                existing_files.add(f.display_name)
    except Exception as e:
        print(f"  Warning: Could not list existing files: {e}")
    return existing_files

def upload_documents(client, store):
    """Upload every article document to the File Search Store."""
    article_files = iter_article_documents()

    if not article_files:
        print(f"\nNo article documents found under {ARTICLES_DIR}")
        return 0

    existing_files = get_existing_files(client, store.name)
    print(f"\nFound {len(existing_files)} existing files in store.")
    
    print(f"\nProcessing {len(article_files)} documents from {ARTICLES_DIR}...")

    uploaded_count = 0
    skipped_count = 0
    
    for idx, file_path in enumerate(article_files, start=1):
        rel_name = file_path.relative_to(ARTICLES_DIR)
        display_name = str(rel_name)
        
        if display_name in existing_files:
            skipped_count += 1
            print(f"  [{idx}/{len(article_files)}] Skipping {display_name} (already exists)")
            continue

        try:
            print(f"  [{idx}/{len(article_files)}] Uploading {display_name}")
            with open(file_path, 'rb') as f:
                client.file_search_stores.upload_to_file_search_store(
                    file_search_store_name=store.name,
                    file=f,
                    config={'display_name': display_name, 'mime_type': 'text/plain'}
                )
            uploaded_count += 1
        except Exception as e:
            print(f"    Error uploading {file_path}: {e}")

    print(f"\nUpload summary: {uploaded_count} uploaded, {skipped_count} skipped.")
    return uploaded_count

def list_store_contents(client, store):
    """List documents in the File Search Store."""
    print(f"\nDocuments in store '{store.display_name}':")
    try:
        docs = list(client.file_search_stores.documents.list(parent=store.name))
        for doc in docs[:10]:  # Show first 10
            print(f"  - {doc.display_name}")
        if len(docs) > 10:
            print(f"  ... and {len(docs) - 10} more documents")
        return len(docs)
    except Exception as e:
        print(f"  Error listing documents: {e}")
        return 0

def main():
    """Main function to set up the AI Act File Search Store."""
    print("=" * 60)
    print("EU AI Act - Gemini File Search Store Setup")
    print("=" * 60)
    
    # Initialize client
    client = create_client()
    print("✓ Gemini API client initialized")
    
    # Create store
    store = create_file_search_store(client)
    
    # Upload documents
    upload_documents(client, store)
    
    # List contents
    doc_count = list_store_contents(client, store)
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print(f"Store Name: {store.name}")
    print(f"Display Name: {store.display_name}")
    print(f"Documents indexed: {doc_count}")
    print("\nYou can now query this store using the Gemini API")
    print("with the FileSearch tool configuration.")
    
    # Save store name for later use
    store_info_path = BASE_DIR / "store_info.txt"
    with open(store_info_path, 'w') as f:
        f.write(f"store_name={store.name}\n")
        f.write(f"display_name={store.display_name}\n")
    print(f"\nStore info saved to: {store_info_path}")

if __name__ == "__main__":
    main()
