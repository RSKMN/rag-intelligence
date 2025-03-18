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

# Assemble the DocumentStore:
data_source = data_source.select(
    data = pw.apply(
        lambda ts, sensor, reading, intensity: 
            f"Timestamp: {ts} | Sensor: {sensor} | Reading: {reading} | Intensity: {intensity}".encode("utf-8"),
        pw.this.timestamp, pw.this.sensor, pw.this.reading, pw.this.intensity
    ),
    _metadata = pw.this.metadata
)

# Set up embedder
embedder = embedders.SentenceTransformerEmbedder(model="all-MiniLM-L12-v2")

# Use BruteForceKnnFactory for retrieval
retriever_factory = BruteForceKnnFactory(embedder=embedder)

# Create DocumentStore
store = DocumentStore(
    docs=data_source,
    retriever_factory=retriever_factory,
)

# Read queries
query = pw.io.fs.read(
    "queries.csv",
    format="csv",
    schema=DocumentStore.RetrieveQuerySchema
)

# Debug prints to show indexed data and loaded queries
stored_data = pw.debug.table_to_pandas(data_source)
print("\nIndexed Data:")
print(stored_data.to_string(index=False))

print("\nQueries Loaded:")
print(query.to_string(index=False))

# Retrieve documents based on the queries
results = store.retrieve_query(query)

# Convert results to Pandas DataFrame for display
results_pd = pw.debug.table_to_pandas(results)

if not results_pd.empty:
    print("\nRetrieved Documents:")
    print(results_pd.to_string(index=False))
else:
    print("\nNo matching documents found.")

pw.run()
