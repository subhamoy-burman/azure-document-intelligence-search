from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
import json
import uuid

# Load settings
with open('local.settings.json', 'r') as f:
    settings = json.load(f)
    env_vars = settings['Values']

# Create search client
search_client = SearchClient(
    endpoint=env_vars["AZURE_AISEARCH_ENDPOINT"],
    index_name=env_vars["SEARCH_INDEX_NAME"],
    credential=AzureKeyCredential(env_vars["AZURE_AISEARCH_KEY"])
)

# Generate a unique document ID
doc_id = str(uuid.uuid4())

# Create a test document using the CORRECT field names from your index
test_doc = {
    "id": doc_id,  # Required key field
    "document_id": "sample-doc-001",  # Optional identifier
    "chunk_text": "This is a test document for Azure AI Search with vector capabilities.",  # Text content field
    "content_vector": [0.1] * 1536  # Vector field - must match 1536 dimensions as specified in your schema
}

print(f"Attempting to upload document with ID: {doc_id}")

try:
    # Upload document
    result = search_client.upload_documents([test_doc])
    print(f"Upload result: {result[0].succeeded}")

    # Get document count
    count = search_client.get_document_count()
    print(f"Document count: {count}")
    
    # Optional: Retrieve the document to verify
    retrieved_doc = search_client.get_document(doc_id)
    print(f"Retrieved document: {retrieved_doc['id']}")
    print(f"Document text: {retrieved_doc['chunk_text'][:50]}...")
    
except Exception as e:
    print(f"Error: {str(e)}")