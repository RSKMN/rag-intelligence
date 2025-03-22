# RAG Intelligence

RAG Intelligence is a Retrieval-Augmented Generation (RAG) system that integrates various components to facilitate seamless interaction with large language models (LLMs), data retrieval, and conversational AI. This README provides an overview of the key scripts in the repository and instructions on how to run them.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Scripts Overview](#scripts-overview)
  - [app.py](#apppy)
  - [server.py](#serverpy)
  - [llm_convo.py](#llm_convopy)
  - [script.py](#scriptpy)
  - [pipeline.py](#pipelinepy)
- [Running the Scripts](#running-the-scripts)
  - [Running app.py](#running-apppy)
  - [Running server.py](#running-serverpy)
  - [Running llm_convo.py](#running-llm_convopy)
  - [Running script.py](#running-scriptpy)
  - [Running pipeline.py](#running-pipelinepy)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optional but recommended)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/RSKMN/rag-intelligence.git
   cd rag-intelligence
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use 'env\Scripts\activate'
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Scripts Overview

### app.py

**Description:** This script sets up a Flask API to handle various endpoints, including processing user queries, handling PDF uploads, and interacting with the LLM for responses.

**Usage:**

- `/ai`: Accepts POST requests with a JSON payload containing a `query` field.
- `/ask_pdf`: Accepts POST requests with a JSON payload containing a `query` field, retrieves relevant information from the PDF data, and returns an answer.
- `/pdf`: Accepts POST requests with a file upload, processes the PDF, and updates the vector store.

### server.py

**Description:** This script initializes and runs a FastAPI server, providing endpoints for health checks and processing prompts. It dynamically loads and initializes example classes that implement methods like `ingest_docs`, `rag_chain`, and `llm_chain`.

**Usage:**

- `/health`: GET endpoint for health checks.
- `/prompt`: POST endpoint that accepts a JSON payload with a list of messages constituting the conversation so far.

### llm_convo.py

**Description:** This script facilitates conversations with the LLM, managing the context and flow of dialogue to maintain coherence and relevance.

**Usage:** Handles user inputs, maintains conversation history, and interacts with the LLM to generate responses.

### script.py

**Description:** This script is designed for fine-tuning the LLaMA model on question-answer pairs, enhancing the model's performance on specific tasks or datasets.

**Usage:** Loads training data, fine-tunes the LLaMA model, and saves the updated model for deployment.

### pipeline.py

**Description:** This script implements the full RAG pipeline, integrating document retrieval and LLM response generation to answer user queries effectively.

**Usage:** Combines retrievers and LLMs to process user queries, retrieve relevant documents, and generate informed responses.

## Running the Scripts

### Running app.py

To run the Flask API:

```bash
python app.py
```

The server will start, and you can interact with the endpoints as described above.

### Running server.py

To run the FastAPI server:

```bash
python server.py
```

The server will start, providing health checks and prompt processing endpoints.

### Running llm_convo.py

To engage in a conversation with the LLM:

```bash
python llm_convo.py
```

Follow the on-screen prompts to input your queries and receive responses from the LLM.

### Running script.py

To fine-tune the LLaMA model:

```bash
python script.py
```

Ensure you have the necessary training data and configurations set up before running this script.

### Running pipeline.py

To execute the RAG pipeline:

```bash
python pipeline.py
```

This will process user queries through the retrieval and generation components to produce responses.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for more details.
