import azure.ai.documentintelligence
import inspect
import importlib
import sys

def check_sdk_version():
    print(f"Azure Document Intelligence SDK version: {azure.ai.documentintelligence.__version__}")
    
    # Try to import AnalyzeDocumentRequest to see its parameters
    try:
        from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
        print("\nAnalyzeDocumentRequest parameters:")
        sig = inspect.signature(AnalyzeDocumentRequest.__init__)
        for param_name, param in sig.parameters.items():
            if param_name != 'self':
                print(f"  - {param_name}")
    except ImportError:
        print("AnalyzeDocumentRequest not found in models module")
    
    # Check begin_analyze_document parameters
    try:
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        print("\nDocumentIntelligenceClient.begin_analyze_document parameters:")
        sig = inspect.signature(DocumentIntelligenceClient.begin_analyze_document)
        for param_name, param in sig.parameters.items():
            if param_name != 'self':
                print(f"  - {param_name}")
    except (ImportError, AttributeError):
        print("Could not inspect begin_analyze_document method")
    
    print("\nInstalled packages:")
    for package in sorted([f"{module.__name__}=={module.__version__}" 
                          for module in [importlib.import_module(pkg) for pkg in sys.modules 
                                         if '.' not in pkg and pkg in sys.modules and hasattr(sys.modules[pkg], '__version__')]
                          if hasattr(module, '__version__')]):
        print(f"  {package}")

if __name__ == "__main__":
    check_sdk_version()
