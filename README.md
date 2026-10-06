# User Memory RAG System

A lightweight RAG-based chatbot that can remember interesting facts about the user during conversations and use those memories to provide more contextual responses.

The system stores user memories in a **JSON file**. When generating a response, the stored memories are provided to the LLM, which determines which information is relevant to the user's current question and uses it as additional context.

## 🎯 Project Goal

The main goal of this project is to explore **prompt versioning and experimentation** in an LLM-based application.

Prompts are separated from the application logic, making it easy to create, test, compare, and switch between different prompt versions without modifying the core code. This provides a practical way to iterate on prompts, evaluate their behavior, and quickly go back to previous versions when needed.

## 🚀 Features

* **User memory** — automatically stores interesting facts learned about the user during conversations.
* **RAG-based responses** — user memories are provided as additional context when generating responses.
* **LLM-based memory selection** — the LLM determines which stored memories are relevant to the current conversation.
* **JSON-based storage** — keeps the memory system simple and easy to inspect or modify.
* **FastAPI backend** — exposes the chatbot through a REST API.
* **Docker support** — provides a containerized version for easier deployment.
* **Versioned prompts** — prompts are stored separately from the application logic.
* **Easy prompt experimentation** — prompts can be modified, tested, compared, and reverted without changing the core application code.

## 🧠 How It Works

The system follows a simple retrieval-augmented architecture:

```text
                    ┌─────────────────┐
                    │   User Message  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │       LLM       │
                    │                 │
                    │ Selects relevant│
                    │    memories     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  JSON Memories  │
                    │                 │
                    │ User facts      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Prompt + Memory │
                    │    + Question   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Generated      │
                    │    Response     │
                    └─────────────────┘
```

### Example

Suppose the system has learned:

```json
{
  "facts": [
    "The user works in AI and automation.",
    "The user likes Python.",
    "The user prefers simple and practical explanations."
  ]
}
```

The user then asks:

> "Can you explain this concept to me?"

The stored memories are passed to the LLM along with the question. The LLM determines which memories are relevant and uses them to generate a more personalized response.

## 🗂️ Memory Storage

User memories are stored in a JSON file rather than a vector database.

This keeps the project lightweight and makes the stored information easy to inspect, modify, and debug during development.

The JSON file acts as the system's external knowledge source, while the LLM handles the selection of relevant information.

## 📝 Prompt Management

Prompts are stored separately from the main application code in a dedicated configuration file.

```text
config/
└── prompts.json
```

This separation makes prompt engineering much easier.

Instead of modifying Python code every time a prompt needs to be changed, different prompt versions can be maintained in the configuration file.

This is particularly useful for:

* Testing different prompts
* Comparing prompt behavior
* Iterating quickly during development
* Switching between prompt versions
* Rolling back to previous prompts
* Experimenting without modifying the application logic

For example:

```text
Prompt v1 → Test
Prompt v2 → Test
Prompt v3 → Test
      ↓
Compare results
      ↓
Keep / modify / revert
```

## 🛠️ Tech Stack

* **Python**
* **FastAPI** — REST API and backend
* **LLM** — memory selection and response generation
* **RAG** — retrieval-augmented generation
* **JSON** — user memory storage
* **Docker** — containerization

## ⚙️ Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file containing the required configuration and API keys.

```env
LLM_API_KEY=your_api_key
```

### 5. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## 🐳 Running with Docker

Build the Docker image:

```bash
docker build -t user-memory-rag .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env user-memory-rag
```

The API will then be available at:

```text
http://localhost:8000
```
