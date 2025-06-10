import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

# Load environment variables from local.settings.json
import json
with open('local.settings.json') as f:
    settings = json.load(f)
    for key, value in settings['Values'].items():
        os.environ[key] = value

# Create OpenAI client
openai_client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version="2023-05-15",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

# Create search client
search_client = SearchClient(
    endpoint=os.environ["AZURE_AISEARCH_ENDPOINT"],
    index_name=os.environ["SEARCH_INDEX_NAME"],
    credential=AzureKeyCredential(os.environ["AZURE_AISEARCH_KEY"])
)

# Generate embedding for search query
query = "Enter your search query here"
response = openai_client.embeddings.create(
    input=query,
    model=os.environ["OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
)
vector = response.data[0].embedding

# Perform vector search
results = search_client.search(
    search_text=None,
    vector={"value": vector, "fields": "contentVector", "k": 3}
)

# Display results
print(f"Search results for: '{query}'")
for result in results:
    print(f"File: {result['fileName']}")
    print(f"Content snippet: {result['content'][:200]}...")
    print("-" * 80)
