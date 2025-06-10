import importlib.metadata
import sys

print("\nPython version:")
print(sys.version)

print("\nInstalled Azure Document Intelligence packages:")
try:
    azure_ai_version = importlib.metadata.version('azure-ai-documentintelligence')
    print(f"azure-ai-documentintelligence: {azure_ai_version}")
except importlib.metadata.PackageNotFoundError:
    print("azure-ai-documentintelligence not found")
    
try:
    azure_ai_formrecognizer = importlib.metadata.version('azure-ai-formrecognizer')
    print(f"azure-ai-formrecognizer: {azure_ai_formrecognizer}")
except importlib.metadata.PackageNotFoundError:
    print("azure-ai-formrecognizer not found")

print("\nAvailable modules:")
import pkgutil
azure_packages = [pkg.name for pkg in pkgutil.iter_modules() if pkg.name.startswith('azure')]
print("\n".join(sorted(azure_packages)))
