# LLM Semantic Memory Assistant

This project is part of my AI engineering learning journey.

As a Product Leader, I wanted to go beyond simply calling an LLM API and actually understand how applications like ChatGPT manage memory. Rather than using an existing framework, I decided to build the memory pipeline myself, one step at a time, so I could understand the engineering decisions behind it.

Every version of this project introduces a new concept. The goal isn't just to build a chatbot—it's to understand how modern AI applications are designed under the hood.

---

## Current Features

The assistant currently supports:

- Conversational chatbot powered by Google Gemini
- Conversation history
- AI-powered memory extraction
- Automatic importance scoring
- Persistent long-term memory using JSON
- Semantic memory retrieval using Sentence Transformers
- Embedding-based similarity search
- Duplicate memory detection
- Dynamic prompt construction using:
  - System instructions
  - Recent conversation history
  - Relevant long-term memories
- Secure API key management using `.env`

---

## How It Works

Every time the user sends a message, the assistant follows this process:

```text
User Message
      │
      ▼
Update Conversation
      │
      ▼
Extract Long-Term Memories (Gemini)
      │
      ▼
Validate Memory
      │
      ▼
Store Memory
      │
      ▼
Generate Embeddings
      │
      ▼
Semantic Memory Search
      │
      ▼
Retrieve Relevant Memories
      │
      ▼
Build Prompt
      │
      ▼
Generate Response (Gemini)
```

Instead of relying on keyword matching, memories are converted into vector embeddings using Sentence Transformers.

When a new question is asked, the assistant searches for memories that are semantically similar to the user's query before sending the final prompt to Gemini.

This means the assistant can retrieve memories based on meaning rather than exact words.

---

## Example

User:

> My dream is to work for a big tech company and earn a six-figure salary.

The memory extractor produces:

```json
[
  {
    "fact": "Dreams of working for a big tech company.",
    "importance": 8
  },
  {
    "fact": "Aims to earn a six-figure salary.",
    "importance": 8
  }
]
```

Later...

User:

> What is my dream?

The assistant retrieves the relevant memories and answers correctly, even after restarting the application.

---

## Tech Stack

- Python
- Google Gemini API
- Sentence Transformers
- PyTorch
- NumPy
- python-dotenv

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/cletusoseikwame/llm-long-term-memory-assistant.git
```

Move into the project:

```bash
cd llm-long-term-memory-assistant
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

Run the assistant:

```bash
python main.py
```

---

## Project Roadmap

### Version 1 ✅

- Gemini chatbot
- Conversation history
- Long-term memory
- Keyword-based memory retrieval

### Version 2 ✅

- AI-powered memory extraction
- Automatic importance scoring
- JSON persistence
- Sentence Transformer embeddings
- Semantic memory retrieval

### Version 3

- ChromaDB integration
- Semantic duplicate detection
- Memory editing and deletion

### Version 4

- Retrieval-Augmented Generation (RAG)
- Document ingestion
- External knowledge retrieval

---

## What I Learned

Building this project helped me understand much more than how to call an LLM API.

Some of the concepts I explored include:

- Prompt engineering
- Long-term memory architectures
- Semantic search
- Vector embeddings
- Similarity search
- JSON persistence
- Object-oriented design
- Separating responsibilities across components
- Building AI systems incrementally

---

## Why I Built This

I'm interested in becoming a stronger AI Product Leader.

For me, that means understanding both product strategy and the engineering behind AI products. Building projects like this helps me better understand the trade-offs involved in designing intelligent systems and makes it much easier to collaborate with engineers.

Rather than following tutorials end-to-end, I prefer building projects from first principles and adding one concept at a time until I understand how everything fits together.

---

## Next Goal

The next step is to extend this project into a Retrieval-Augmented Generation (RAG) system by allowing the assistant to retrieve information from external documents instead of relying only on conversational memory.

---

## About Me

I'm a Product Leader with a growing interest in AI engineering.

I'm learning Python and modern AI engineering by building practical projects that help me understand how intelligent systems are designed, with the goal of becoming a more technical product leader capable of building and leading AI products.