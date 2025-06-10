import os
import json
import base64
import traceback
import logging
import uuid
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
with open('local.settings.json', 'r') as f:
    settings = json.load(f)
    for key, value in settings['Values'].items():
        os.environ[key] = value

def create_sample_pdf(filename="test_document.pdf"):
    """Create a sample PDF file for testing"""
    logging.info(f"Creating sample PDF file: {filename}")
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "This is a test document for Azure Document Intelligence API")
    c.drawString(100, 730, f"Generated on: {uuid.uuid4()}")
    c.drawString(100, 710, "Sample content for testing document processing")
    c.save()
    logging.info(f"Sample PDF created successfully at {filename}")
    return filename

def test_analyze_document():
    try:
        # Create a sample PDF document
        test_doc_path = create_sample_pdf()
        
        # Read the document bytes
        with open(test_doc_path, "rb") as f:
            document_bytes = f.read()
        
        logging.info(f"Test document size: {len(document_bytes)} bytes")
        
        # Get credentials from settings
        endpoint = os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"]
        key = os.environ["DOCUMENT_INTELLIGENCE_KEY"]
        
        logging.info(f"Creating Document Intelligence client with endpoint: {endpoint}")
        document_intelligence_client = DocumentIntelligenceClient(
            endpoint=endpoint, 
            credential=AzureKeyCredential(key)
        )
          # OPTION 1: Use AnalyzeDocumentRequest with bytes_source parameter
        logging.info("TESTING OPTION 1: AnalyzeDocumentRequest with bytes_source")
        try:
            # Create the analyze request with the correct parameter name
            analyze_request = AnalyzeDocumentRequest(
                bytes_source=document_bytes  # Use bytes_source instead of base64Source
            )
            
            # Use analyze_request parameter
            poller = document_intelligence_client.begin_analyze_document(
                model_id="prebuilt-layout",
                analyze_request=analyze_request
            )
            
            result = poller.result()
            logging.info(f"Option 1 result: Document has {len(result.pages)} page(s)")
            logging.info(f"Content: {result.content[:200]}...")
        except Exception as e:
            logging.error(f"Option 1 failed: {str(e)}")
              # OPTION 2: Use base64Source directly
        logging.info("TESTING OPTION 2: Using base64Source directly")
        try:
            # Convert bytes to base64
            base64_encoded = base64.b64encode(document_bytes).decode('utf-8')
            
            # Create a JSON object manually using the expected parameter names
            request_json = {"base64Source": base64_encoded}
            
            # Pass the JSON directly
            poller = document_intelligence_client.begin_analyze_document(
                model_id="prebuilt-layout",
                analyze_request=request_json
            )
            
            result = poller.result()
            logging.info(f"Option 2 result: Document has {len(result.pages)} page(s)")
            logging.info(f"Content: {result.content[:200]}...")
        except Exception as e:
            logging.error(f"Option 2 failed: {str(e)}")
        return True
    
    except Exception as e:
        logging.error(f"Error in test_analyze_document: {str(e)}")
        logging.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_analyze_document()
    if success:
        print("Test completed successfully!")
    else:
        print("Test failed! See logs for details.")
