from pipeline import store  # Import the DocumentStore built in pipeline.py
from pathway.xpacks.llm.servers import DocumentStoreServer

# Set up and start the REST API server on port 8765.
PATHWAY_PORT = 8765
server = DocumentStoreServer(
    host="0.0.0.0",  # Listen on all interfaces
    port=PATHWAY_PORT,
    document_store=store,
)

# Run the server in blocking mode.
server.run(threaded=False, with_cache=False)
