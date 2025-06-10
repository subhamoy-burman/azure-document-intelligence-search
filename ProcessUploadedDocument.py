# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(ProcessUploadedDocument) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
import os
import io
import json
import uuid
import traceback
from datetime import datetime
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
from azure.search.documents import SearchClient

# Create the blueprint
ProcessUploadedDocument = func.Blueprint()

@ProcessUploadedDocument.blob_trigger(arg_name="myblob", path="knowledge-docs/{name}",
                               connection="aligndataengineering_STORAGE") 
def process_uploaded_document(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processing blob\n"
                f"Name: {myblob.name}\n"
                f"Blob Size: {myblob.length} bytes")
    
    try:
        # Log start of processing
        logging.info(f"=== STARTING PROCESSING FOR: {myblob.name} ===")
        
        # 1. Read document from blob storage
        document_bytes = myblob.read()
        logging.info(f"Successfully read {len(document_bytes)} bytes from blob")
        
        # Check if this is a PDF or other supported document type
        file_extension = os.path.splitext(myblob.name)[1].lower()
        supported_extensions = ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls']
        
        if file_extension not in supported_extensions:
            logging.warning(f"Unsupported file type: {file_extension}. Skipping processing.")
            return
        
        logging.info(f"File extension {file_extension} is supported, proceeding with processing")
            
        # 2. Process document with Document Intelligence
        logging.info("Starting Document Intelligence analysis")
        extracted_text = analyze_document(document_bytes)
        
        if not extracted_text or len(extracted_text.strip()) == 0:
            logging.warning(f"No text extracted from document: {myblob.name}. Skipping further processing.")
            return
        
        logging.info(f"Successfully extracted {len(extracted_text)} characters of text")
            
        # 3. Generate embeddings using Azure OpenAI
        logging.info("Starting embedding generation with Azure OpenAI")
        embeddings = generate_embeddings(extracted_text)
        logging.info(f"Successfully generated embeddings with dimension: {len(embeddings)}")
        
        # 4. Create search document and add to Azure AI Search
        logging.info("Adding document to Azure AI Search")
        add_to_search_index(myblob.name, extracted_text, embeddings)
        
        logging.info(f"=== SUCCESSFULLY PROCESSED DOCUMENT: {myblob.name} ===")
    
    except Exception as e:
        logging.error(f"Error processing document {myblob.name}: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        # Consider storing failed documents info in a separate container or queue
        raise

def analyze_document(document_bytes):
    """Analyze document using Azure Document Intelligence"""
    try:
        import io
        from azure.core.exceptions import HttpResponseError
        
        endpoint = os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"]
        key = os.environ["DOCUMENT_INTELLIGENCE_KEY"]
        
        logging.info(f"Creating Document Intelligence client with endpoint: {endpoint}")
        document_intelligence_client = DocumentIntelligenceClient(
            endpoint=endpoint, 
            credential=AzureKeyCredential(key)
        )
        
        logging.info("Sending document to Azure Document Intelligence for analysis")
        # Use AnalyzeDocumentRequest with bytes_source parameter
        from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
        
        analyze_request = AnalyzeDocumentRequest(
            bytes_source=document_bytes
        )
        
        poller = document_intelligence_client.begin_analyze_document(
            model_id="prebuilt-layout",
            analyze_request=analyze_request
        )
        
        logging.info("Waiting for document analysis to complete")
        result = poller.result()
        
        # Extract text from the document
        text_content = ""
        for page in result.pages:
            for line in page.lines:
                text_content += line.content + "\n"
        
        return text_content
    
    except Exception as e:
        logging.error(f"Error in analyze_document: {str(e)}")
        logging.error(traceback.format_exc())
        raise

def generate_embeddings(text):
    """Generate embeddings using Azure OpenAI"""
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_KEY"]
    deployment_name = os.environ["OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version="2023-05-15",
        azure_endpoint=endpoint
    )
    
    response = client.embeddings.create(
        input=text,
        model=deployment_name
    )
    
    return response.data[0].embedding

def add_to_search_index(doc_name, content, embeddings):
    """Add document to Azure AI Search index"""
    search_endpoint = os.environ["AZURE_AISEARCH_ENDPOINT"]
    search_key = os.environ["AZURE_AISEARCH_KEY"]
    index_name = os.environ["SEARCH_INDEX_NAME"]
    
    # Create search client
    search_client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(search_key)
    )
    
    # Generate a unique document ID
    doc_id = str(uuid.uuid4())
    
    # Create the document - use embeddings directly in a vector field
    document = {
        "id": doc_id,
        "content": content,
        "fileName": doc_name,
        "contentVector": embeddings,  # Use embeddings directly without Vector class
        "processed_dt": datetime.utcnow().isoformat()
    }
    
    # Upload to search index
    search_client.upload_documents([document])
    
    logging.info(f"Document {doc_name} indexed with ID {doc_id}")