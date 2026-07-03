# Hemanth RAG API

Personal RAG API workspace for Nallappagari Hemanth Sai, built on an MIT-licensed FastAPI and LangChain retrieval service.

## Attribution

This project is derived from `danny-avila/rag_api`. The original MIT license and copyright notice are retained in `LICENSE`.

## Overview
This project integrates Langchain with FastAPI in an Asynchronous, Scalable manner, providing a framework for document indexing and retrieval using MongoDB Atlas Vector Search.

Files are organized into embeddings by `file_id`. The primary use case is for integration with [LibreChat](https://librechat.ai), but this simple API can be used for any ID-based use case.

The main reason to use the ID approach is to work with embeddings on a file-level. This makes for targeted queries when combined with file metadata stored in a database, such as is done by LibreChat.

The API will evolve over time to employ different querying/re-ranking methods, embedding models, and vector stores.

## Features
- **Document Management**: Methods for adding, retrieving, and deleting documents.
- **Vector Store**: Utilizes Langchain's vector store for efficient document retrieval.
- **Asynchronous Support**: Offers async operations for enhanced performance.

## Setup

### Getting Started

- **Configure `.env` file based on [section below](#environment-variables)**
- **Setup MongoDB Atlas Vector Search:**
  - Add your Atlas connection string to `.env` as `ATLAS_MONGO_DB_URI`.
  - Create the vector search index described in [Use Atlas MongoDB as Vector Database](#use-atlas-mongodb-as-vector-database).
- **Run API**:
  - Docker: `docker compose up`
    - or, use docker just for RAG API: `docker compose -f ./api-compose.yaml up`
  - Local:
    - Make sure `.env` contains `VECTOR_DB_TYPE=atlas-mongo` and `ATLAS_MONGO_DB_URI`
    - Run the following commands (preferably in a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/))
```bash
pip install -r requirements.txt
uvicorn main:app
```

### Clean Install (Local Development)

To do a clean reinstall of all dependencies (e.g., after updating `requirements.txt`):

```bash
# Remove existing virtual environment and recreate it
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For the lite version (without sentence_transformers/huggingface):

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.lite.txt
```

For Docker, rebuild without cache:

```bash
docker compose build --no-cache
```

### Environment Variables

The following environment variables are required to run the application:

- `RAG_OPENAI_API_KEY`: The API key for OpenAI API Embeddings (if using default settings).
    - Note: `OPENAI_API_KEY` will work but `RAG_OPENAI_API_KEY` will override it in order to not conflict with LibreChat setting.
- `RAG_OPENAI_BASEURL`: (Optional) The base URL for your OpenAI API Embeddings
- `RAG_OPENAI_PROXY`: (Optional) Proxy for OpenAI API Embeddings
    - Note: When using with LibreChat, you can also set `HTTP_PROXY` and `HTTPS_PROXY` environment variables in the `docker-compose.override.yml` file (see [Proxy Configuration](#proxy-configuration) section below)
- `VECTOR_DB_TYPE`: (Optional) select vector database type, default to `atlas-mongo`.
- `ATLAS_MONGO_DB_URI`: MongoDB Atlas connection string used when `VECTOR_DB_TYPE=atlas-mongo`.
- `ATLAS_MONGO_DB_NAME`: (Optional) the MongoDB database name used when the connection URI does not include one.
- `ATLAS_SEARCH_INDEX`: (Optional) the name of the vector search index if using Atlas MongoDB, defaults to `vector_index`.
- `RAG_HOST`: (Optional) The hostname or IP address where the API server will run. Defaults to "0.0.0.0"
- `RAG_PORT`: (Optional) The port number where the API server will run. Defaults to port 8000.
- `JWT_SECRET`: (Optional) The secret key used for verifying JWT tokens for requests.
  - The secret is only used for verification. This basic approach assumes a signed JWT from elsewhere.
  - Omit to run API without requiring authentication

- `COLLECTION_NAME`: (Optional) The name of the collection in the vector store. Default value is "hemanth_rag_collection".
- `CHUNK_SIZE`: (Optional) The size of the chunks for text processing. Default value is "1500".
- `CHUNK_OVERLAP`: (Optional) The overlap between chunks during text processing. Default value is "100".
- `EMBEDDING_BATCH_SIZE`: (Optional) Number of document chunks to process per batch. Set to `0` (default) to disable batching. Recommended value is `750` for `text-embedding-3-small`.
- `EMBEDDING_MAX_QUEUE_SIZE`: (Optional) Maximum number of batches to buffer in memory during async processing. Default value is "3".
- `RAG_DISTANCE_THRESHOLD`: Ignored under `VECTOR_DB_TYPE=atlas-mongo`, because Atlas returns a similarity score with different semantics.
- `RAG_UPLOAD_DIR`: (Optional) The directory where uploaded files are stored. Default value is "./uploads/".
- `PDF_EXTRACT_IMAGES`: (Optional) A boolean value indicating whether to extract images from PDF files. Default value is "False".
- `DEBUG_RAG_API`: (Optional) Set to "True" to show more verbose logging output in the server console.
- `CONSOLE_JSON`: (Optional) Set to "True" to log as json for Cloud Logging aggregations
- `EMBEDDINGS_PROVIDER`: (Optional) either "openai", "bedrock", "azure", "huggingface", "huggingfacetei", "google_genai", "vertexai", or "ollama", where "huggingface" uses sentence_transformers; defaults to "openai"
- `EMBEDDINGS_MODEL`: (Optional) Set a valid embeddings model to use from the configured provider.
    - **Defaults**
    - openai: "text-embedding-3-small"
    - azure: "text-embedding-3-small" (will be used as your Azure Deployment)
    - huggingface: "sentence-transformers/all-MiniLM-L6-v2"
    - huggingfacetei: "http://huggingfacetei:3000". Hugging Face TEI uses model defined on TEI service launch.
    - vertexai: "gemini-embedding-001"
    - ollama: "nomic-embed-text"
    - bedrock: "amazon.titan-embed-text-v1"
    - google_genai: "gemini-embedding-001"
- `EMBEDDINGS_CHUNK_SIZE`: (Optional) The chunk size used by the OpenAI and Azure embeddings clients to limit the number of inputs per request. Default value is `200`.
- `EMBEDDINGS_DIMENSIONS`: (Optional) Output vector size to request from the embedding model. Only honored by the `openai` and `azure` providers, and only supported by `text-embedding-3-*` models. Leave unset to use the model's native dimensionality (1536 for `text-embedding-3-small`, 3072 for `text-embedding-3-large`). Setting a smaller value (e.g. `512`, `1024`) trades some retrieval quality for lower storage cost and faster similarity search.
- `RAG_AZURE_OPENAI_API_VERSION`: (Optional) Default is `2023-05-15`. The version of the Azure OpenAI API.
- `RAG_AZURE_OPENAI_API_KEY`: (Optional) The API key for Azure OpenAI service.
    - Note: `AZURE_OPENAI_API_KEY` will work but `RAG_AZURE_OPENAI_API_KEY` will override it in order to not conflict with LibreChat setting.
- `RAG_AZURE_OPENAI_ENDPOINT`: (Optional) The endpoint URL for Azure OpenAI service, including the resource.
    - Example: `https://YOUR_RESOURCE_NAME.openai.azure.com`.
    - Note: `AZURE_OPENAI_ENDPOINT` will work but `RAG_AZURE_OPENAI_ENDPOINT` will override it in order to not conflict with LibreChat setting.
- `HF_TOKEN`: (Optional) if needed for `huggingface` option.
- `OLLAMA_BASE_URL`: (Optional) defaults to `http://ollama:11434`.
- `ATLAS_SEARCH_INDEX`: (Optional) the name of the vector search index if using Atlas MongoDB, defaults to `vector_index`
- `MONGO_VECTOR_COLLECTION`: Deprecated for MongoDB, please use `ATLAS_SEARCH_INDEX` and `COLLECTION_NAME`
- `AWS_DEFAULT_REGION`: (Optional) defaults to `us-east-1`
- `AWS_ACCESS_KEY_ID`: (Optional) needed for bedrock embeddings
- `AWS_SECRET_ACCESS_KEY`: (Optional) needed for bedrock embeddings
- `GOOGLE_API_KEY`, `GOOGLE_KEY`, `RAG_GOOGLE_API_KEY`: (Optional) Google API key for Google GenAI embeddings. Priority order: RAG_GOOGLE_API_KEY > GOOGLE_KEY > GOOGLE_API_KEY
- `AWS_SESSION_TOKEN`: (Optional) may be needed for bedrock embeddings
- `GOOGLE_APPLICATION_CREDENTIALS`: (Optional) needed for Google VertexAI embeddings. This should be a path to a service account credential file in JSON format.
- `GOOGLE_CLOUD_PROJECT`: (Optional) Google Cloud project ID, needed for VertexAI embeddings.
- `GOOGLE_CLOUD_LOCATION`: (Optional) Google Cloud region for VertexAI embeddings. Defaults to `us-central1`.
- `RAG_CHECK_EMBEDDING_CTX_LENGTH` (Optional) Default is true, disabling this will send raw input to the embedder, use this for custom embedding models.

Make sure to set these environment variables before running the application. You can set them in a `.env` file or as system environment variables.

### Embedding Batch Processing

For large files, you can enable batched embedding processing to reduce memory consumption. This is particularly useful in memory-constrained environments like Kubernetes pods with memory limits.

#### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `EMBEDDING_BATCH_SIZE` | `0` | Number of document chunks to process per batch. `0` disables batching (original behavior). |
| `EMBEDDING_MAX_QUEUE_SIZE` | `3` | Maximum number of batches to buffer in memory during async processing. |

#### Recommended Settings

For `text-embedding-3-small` model:
- `EMBEDDING_BATCH_SIZE=750` - Good balance of throughput and memory

For memory-constrained environments (< 2GB RAM):
- `EMBEDDING_BATCH_SIZE=100-250`

For high-throughput environments:
- `EMBEDDING_BATCH_SIZE=1000-2000`
- `EMBEDDING_MAX_QUEUE_SIZE=5`

#### Behavior

When `EMBEDDING_BATCH_SIZE > 0`:
- Documents are processed in batches of the specified size
- Each batch is embedded and inserted before the next batch starts
- On failure, successfully inserted documents are rolled back
- Memory usage is bounded by `EMBEDDING_BATCH_SIZE * EMBEDDING_MAX_QUEUE_SIZE`

When `EMBEDDING_BATCH_SIZE = 0` (default):
- All documents are processed at once (original behavior)
- Better for small files or memory-rich environments

### Use Atlas MongoDB as Vector Database

This project uses [Atlas MongoDB](https://www.mongodb.com/products/platform/atlas-vector-search) as the vector database. Set the following environment variables:

```env
VECTOR_DB_TYPE=atlas-mongo
ATLAS_MONGO_DB_URI=<mongodb+srv://...>
ATLAS_MONGO_DB_NAME=hemanth_rag
COLLECTION_NAME=<vector collection>
ATLAS_SEARCH_INDEX=<vector search index>
```

The `ATLAS_MONGO_DB_URI` could be the same or different from what is used by LibreChat. If the URI does not include a default database path, set `ATLAS_MONGO_DB_NAME` to the target database name. Even if it is the same, the `$COLLECTION_NAME` collection needs to be a completely new one, separate from all collections used by LibreChat. In addition,  create a vector search index for collection above (remember to assign `$ATLAS_SEARCH_INDEX`) with the following json:

```json
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "file_id",
      "type": "filter"
    }
  ]
}
```

Follow one of the [four documented methods](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/#procedure) to create the vector index.

#### Create a `file_id` Index (recommended)

We recommend creating a standard MongoDB index on `file_id` to keep lookups fast. After creating the collection, run the following once (via Atlas UI, Compass, or `mongosh`):

```javascript
db.getCollection("<COLLECTION_NAME>").createIndex({ file_id: 1 })
```

Replace `<COLLECTION_NAME>` with the same collection used by the RAG API. This ensures lookups remain fast even as the number of embedded documents grows.


### Proxy Configuration

When using the RAG API with LibreChat and you need to configure proxy settings, you can set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables in the [`docker-compose.override.yml`](https://www.librechat.ai/docs/configuration/docker_override) file (from the LibreChat repository):

```yaml
rag_api:
    environment:
        - HTTP_PROXY=<your-proxy>
        - HTTPS_PROXY=<your-proxy>
```

This configuration will ensure that all HTTP/HTTPS requests from the RAG API container are routed through your specified proxy server.


### Dev notes:

#### Running Tests

##### Prerequisites

Install test dependencies:

```bash
pip install -r test_requirements.txt
```

##### Running All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage (if pytest-cov is installed)
pytest --cov=app
```

##### Running Specific Test Files

```bash
# Run batch processing unit tests
pytest tests/test_batch_processing.py -v

# Run batch processing integration tests (memory optimization tests)
pytest tests/test_batch_processing_integration.py -v

# Run main API tests
pytest tests/test_main.py -v
```

##### Running Tests by Category

```bash
# Run only integration tests (marked with @pytest.mark.integration)
pytest -m integration -v

# Skip integration tests
pytest -m "not integration" -v

# Run only async tests
pytest -k "async" -v
```

##### Test Categories

| Test File | Description |
|-----------|-------------|
| `test_batch_processing.py` | Unit tests for batch processing functions |
| `test_batch_processing_integration.py` | Memory optimization and integration tests |
| `test_main.py` | API endpoint tests |
| `test_config.py` | Configuration tests |
| `test_middleware.py` | Middleware tests |
| `test_models.py` | Model tests |

##### Memory Optimization Tests

The `test_batch_processing_integration.py` file includes tests that verify the memory optimization behavior:

- **`test_memory_bounded_by_batch_size`**: Verifies that the number of documents in memory at any time is bounded by `EMBEDDING_BATCH_SIZE`
- **`test_memory_tracking_with_tracemalloc`**: Uses Python's `tracemalloc` to monitor memory usage during batch processing
- **`test_sync_memory_bounded_by_batch_size`**: Same verification for the synchronous code path

Run memory tests specifically:

```bash
pytest tests/test_batch_processing_integration.py::TestMemoryOptimization -v
pytest tests/test_batch_processing_integration.py::TestSyncBatchedMemory -v
```

#### Installing pre-commit formatter

Run the following commands to install pre-commit formatter, which uses [black](https://github.com/psf/black) code formatter:

```bash
pip install pre-commit
pre-commit install
```

