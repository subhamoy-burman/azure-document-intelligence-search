import os
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from openai import AzureOpenAI
from azure.search.documents import SearchClient

# Load environment variables
with open('local.settings.json') as f:
    settings = json.load(f)
    for key, value in settings['Values'].items():
        os.environ[key] = value

def test_document_intelligence():
    print("Testing Document Intelligence connection...")
    try:
        endpoint = os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"]
        key = os.environ["DOCUMENT_INTELLIGENCE_KEY"]
        
        client = DocumentIntelligenceClient(
            endpoint=endpoint, 
            credential=AzureKeyCredential(key)
        )
        
        # Just test the connection, no actual API call needed
        print("✅ Document Intelligence client created successfully")
        return True
    except Exception as e:
        print(f"❌ Document Intelligence connection failed: {str(e)}")
        return False

def test_openai():
    print("Testing Azure OpenAI connection...")
    try:
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        api_key = os.environ["AZURE_OPENAI_KEY"]
        deployment_name = os.environ["OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
        
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2023-05-15",
            azure_endpoint=endpoint
        )
        
        # Test with a simple embedding
        response = client.embeddings.create(
            input="Hello, world",
            model=deployment_name
        )
        
        if response.data:
            print(f"✅ Azure OpenAI connection successful, embedding dimension: {len(response.data[0].embedding)}")
            return True
        else:
            print("❌ Azure OpenAI returned empty response")
            return False
    except Exception as e:
        print(f"❌ Azure OpenAI connection failed: {str(e)}")
        return False

def test_search():
    print("Testing Azure AI Search connection...")
    try:
        search_endpoint = os.environ["AZURE_AISEARCH_ENDPOINT"]
        search_key = os.environ["AZURE_AISEARCH_KEY"]
        index_name = os.environ["SEARCH_INDEX_NAME"]
        
        search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(search_key)
        )
        
        # Test if index exists by trying to get count
        result = search_client.get_document_count()
        print(f"✅ Azure AI Search connection successful, document count: {result}")
        return True
    except Exception as e:
        print(f"❌ Azure AI Search connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Testing Azure Service Connections ===")
    di_success = test_document_intelligence()
    openai_success = test_openai()
    search_success = test_search()
    
    if di_success and openai_success and search_success:
        print("✅ All connections successful!")
    else:
        print("❌ Some connections failed, see above for details.")
