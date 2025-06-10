import os
import json
import base64
import traceback
import logging
import io
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

# Set up more detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load environment variables
with open('local.settings.json') as f:
    settings = json.load(f)
    for key, value in settings['Values'].items():
        os.environ[key] = value

def test_document_intelligence():
    print("Testing Document Intelligence connection and API call...")
    try:
        # Debug point 1 - Check environment variables
        endpoint = os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"]
        key = os.environ["DOCUMENT_INTELLIGENCE_KEY"]
        print(f"Endpoint: {endpoint}")
        print(f"Key (partial): {key[:5]}...")
        
        # Create client
        client = DocumentIntelligenceClient(
            endpoint=endpoint, 
            credential=AzureKeyCredential(key)
        )
        
        # Create a simple text file to test with
        sample_text = "This is a sample document for Document Intelligence API test."
        test_doc_path = "test_document.txt"
        
        with open(test_doc_path, "w") as f:
            f.write(sample_text)
        
        # Read the document bytes
        with open(test_doc_path, "rb") as f:
            document_bytes = f.read()
        
        # Debug point 2 - Check document
        print(f"Document size: {len(document_bytes)} bytes")
        
        # Debug point 3 - Right before API call
        print("About to call API with model_id=prebuilt-layout...")
        
        # Test the API call - using file content directly
        with open(test_doc_path, "rb") as f:
            # Based on the function signature, use analyze_request not body or document
            poller = client.begin_analyze_document(
                model_id="prebuilt-layout",
                analyze_request=f
            )
        
        # Debug point 4 - After API call started
        print("API call started, waiting for result...")
        
        # Wait for the result
        result = poller.result()
        print("API call successful!")
        
        # Print results
        if result.pages and len(result.pages) > 0:
            print(f"Document has {len(result.pages)} page(s)")
            for page in result.pages:
                if page.lines:
                    for line in page.lines:
                        print(f"Line: {line.content}")
        
        return True
    except Exception as e:
        print(f"Error testing Document Intelligence: {str(e)}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Debug entry point
    print("=== Starting Document Intelligence Test with Debug Info ===")
    test_document_intelligence()
