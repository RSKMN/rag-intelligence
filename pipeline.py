import pathway as pw
from pathway.xpacks.llm import embedders
from pathway.stdlib.indexing.nearest_neighbors import BruteForceKnnFactory
from pathway.xpacks.llm.document_store import DocumentStore

# Define schema (keep reading as a string)
class InputSchema(pw.Schema):
    timestamp: str = pw.column_definition(primary_key=True)
    sensor: str
    reading: str  # Keep as str
    intensity: float
    metadata: dict

# Read the JSONL file in streaming mode and explicitly convert "reading" to a string
data_source = pw.io.jsonlines.read(
    "/root/RAG/simulated_data.jsonl",
    schema=InputSchema,
    with_metadata=True,
    mode="streaming"   # Enable streaming mode
).select(
    timestamp=pw.this.timestamp,
    sensor=pw.this.sensor,
    reading=pw.apply(str, pw.this.reading),  # Explicit conversion to string
    intensity=pw.this.intensity,
    metadata=pw.this.metadata
)

# Assemble the DocumentStore by creating a 'data' column (as bytes) and mapping metadata.
data_source = data_source.select(
    data = pw.apply(
        lambda ts, sensor, reading, intensity: 
            f"Timestamp: {ts} | Sensor: {sensor} | Reading: {reading} | Intensity: {intensity}".encode("utf-8"),
        pw.this.timestamp, pw.this.sensor, pw.this.reading, pw.this.intensity
    ),
    _metadata = pw.this.metadata
)

# Set up embedder and retriever factory
embedder = embedders.SentenceTransformerEmbedder(model="all-MiniLM-L12-v2")
retriever_factory = BruteForceKnnFactory(embedder=embedder)

# Create the DocumentStore
store = DocumentStore(
    docs=data_source,
    retriever_factory=retriever_factory,
)

# Optional: If you run pipeline.py directly, you can run the computation.
if __name__ == "__main__":
    # Optionally print some debug info
    stored_data = pw.debug.table_to_pandas(data_source)
    print("\nIndexed Data:")
    print(stored_data.to_string(index=False))
    
    # This call is blocking; if you run this file directly, it starts the pipeline.
    pw.run()
