import azure.functions as func
import os
import logging

# Import the blueprint directly
from ProcessUploadedDocument import ProcessUploadedDocument

# Create the FunctionApp instance
app = func.FunctionApp()

# Validate required settings before registering the function
required_settings = [
    "DOCUMENT_INTELLIGENCE_ENDPOINT",
    "DOCUMENT_INTELLIGENCE_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_KEY",
    "OPENAI_EMBEDDING_DEPLOYMENT_NAME",
    "AZURE_AISEARCH_ENDPOINT",
    "AZURE_AISEARCH_KEY",
    "SEARCH_INDEX_NAME"
]

missing_settings = [setting for setting in required_settings if not os.environ.get(setting)]

if missing_settings:
    logging.error(f"Missing required application settings: {', '.join(missing_settings)}")
    logging.warning("Function may not work correctly without these settings")

# Register the blueprint properly
app.register_blueprint(ProcessUploadedDocument)
