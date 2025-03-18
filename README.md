# RAG Intelligence: Mimicking Human-Like Memory with Pathway

**RAG Intelligence** is a real-time retrieval-augmented generation (RAG) system that simulates core human cognitive functions—particularly episodic memory recall—using [Pathway](https://pathway.com/). Inspired by neuroscience and cognitive science research, this project ingests text-based sensor data, indexes it with semantic embeddings, and offers interactive, human-like memory recall via a REST API and a Streamlit dashboard.

## Features

- **Real-Time Data Ingestion:**  
  Continuously monitors a JSONL file using Pathway in streaming mode.

- **Episodic Memory Simulation:**  
  Mimics human-like memory by indexing past sensor interactions with rich contextual details such as timestamp, sensor type, reading, intensity, and metadata.

- **Semantic Retrieval:**  
  Leverages SentenceTransformer embeddings and a BruteForceKnn retrieval factory to fetch contextually relevant documents based on natural language queries.

- **REST API Server:**  
  Exposes memory retrieval endpoints via a DocumentStoreServer on port 8765.

- **User-Friendly Dashboard:**  
  Provides a Streamlit dashboard for interactive query submission and visualization of retrieved memories.

- **Local LLM Integration (Optional):**  
  Enhances responses using a local HuggingFace model (e.g., distilgpt2) to generate natural language responses without requiring an external API key.

## Architecture Overview

1. **Pipeline:**  
   - **Data Ingestion:** Reads sensor data from `simulated_data.jsonl` in streaming mode.
   - **Preprocessing:** Converts raw sensor entries into a unified text field (`data`) and maps metadata for indexing.
   - **Indexing:** Uses Pathway’s DocumentStore, BruteForceKnnFactory, and SentenceTransformerEmbedder to create a semantic index.

2. **REST API Server:**  
   - Runs a DocumentStoreServer that exposes a `/v1/retrieve` endpoint to handle memory recall queries.

3. **Dashboard:**  
   - Built using Streamlit, it allows users to interact with the system by entering queries and viewing both raw and enhanced responses.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- [Pathway](https://github.com/pathway-com/pathway)
- A virtual environment (recommended)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/RSKMN/rag-intelligence.git
   cd rag-intelligence

## Set Up Your Virtual Environment:
     python -m venv myenv
    source myenv/bin/activate  # On Windows: myenv\Scripts\activate

## Install Dependencies:
pip install -r requirements.txt

# 1. Run the Pipeline
python pipeline.py


# 2. Run the REST API Server
python server.py


 # 3. Run the Streamlit Dashboard
streamlit run app.py






