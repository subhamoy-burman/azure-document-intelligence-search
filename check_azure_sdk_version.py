import os
import sys
import importlib.metadata

def check_sdk_versions():
    """Check the installed Azure SDK versions"""
    print("Python version:", sys.version)
    
    # Print Azure Document Intelligence SDK version
    try:
        di_version = importlib.metadata.version('azure-ai-documentintelligence')
        print(f"Azure AI Document Intelligence SDK version: {di_version}")
    except importlib.metadata.PackageNotFoundError:
        print("Azure AI Document Intelligence SDK not found")
    
    # Print Azure Search SDK version
    try:
        search_version = importlib.metadata.version('azure-search-documents')
        print(f"Azure Search Documents SDK version: {search_version}")
    except importlib.metadata.PackageNotFoundError:
        print("Azure Search Documents SDK not found")
    
    # Print OpenAI SDK version
    try:
        openai_version = importlib.metadata.version('openai')
        print(f"OpenAI SDK version: {openai_version}")
    except importlib.metadata.PackageNotFoundError:
        print("OpenAI SDK not found")

if __name__ == "__main__":
    check_sdk_versions()
    
    # Try to inspect the DocumentIntelligenceClient class
    try:
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        import inspect
        
        print("\nDocumentIntelligenceClient.begin_analyze_document parameters:")
        signature = inspect.signature(DocumentIntelligenceClient.begin_analyze_document)
        for param_name, param in signature.parameters.items():
            if param_name != 'self':
                print(f"  - {param_name}: {param.annotation}")
                if param.default is not inspect.Parameter.empty:
                    print(f"    Default value: {param.default}")
    except Exception as e:
        print(f"Error inspecting DocumentIntelligenceClient: {str(e)}")
