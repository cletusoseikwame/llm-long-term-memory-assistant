# LLM Long-Term Memory Assistant

 A Python project exploring long-term memory architectures for Large Language Model (LLM) applications using the Google Gemini API.

I built this project to deepen my understanding of the architecture behind modern AI systems. As a Product Leader building AI-enabled products, I believe it's increasingly important to understand not only what AI can do, but also how these systems are designed and implemented.

Rather than simply integrating an LLM API, I wanted to build the memory pipeline myself—from storing facts to retrieving relevant information and constructing prompts—so I could better understand the engineering decisions behind intelligent assistants.

This project is being developed incrementally, with each version introducing a new AI engineering concept.

---

# Current Features

The current implementation includes:

* Conversational chatbot powered by Google's Gemini API
* Conversation history management
* Fact extraction from user messages
* Keyword extraction with stop-word filtering
* Long-term memory storage
* Duplicate memory detection
* Keyword-based memory retrieval
* Dynamic prompt construction using:

  * System instructions
  * Recent conversation history
  * Retrieved memories
* Secure API key management using `.env`
* Git version control

---

# How It Works

For every user message, the assistant follows this pipeline:

```text
User Message
        ↓
Update Conversation
        ↓
Select Recent Messages
        ↓
Extract Facts
        ↓
Assign Importance
        ↓
Store Memory
        ↓
Extract Keywords
        ↓
Search Long-Term Memory
        ↓
Build Prompt
        ↓
Send to Gemini
        ↓
Generate Response
```

The current version retrieves memories using keyword matching. Future iterations will introduce semantic retrieval using embeddings and vector databases.

---

# Tech Stack

* Python 3
* Google Gemini API
* python-dotenv
* Git & GitHub

---

# Why I Built This

The next generation of AI Product Leaders will need more than an understanding of user needs and business strategy—they'll also need a solid grasp of how AI systems are engineered.

This project is part of my effort to build that technical depth by implementing the core building blocks behind LLM-powered applications, including:

* Prompt engineering
* Conversation management
* Long-term memory
* Retrieval pipelines
* Context management
* LLM application architecture

My goal is to become a stronger product leader by understanding the technical trade-offs involved in designing and building AI products.

---

# Running the Project

Clone the repository:

```bash
git clone https://github.com/Cletjunior/llm-long-term-memory-assistant.git
```

Navigate into the project:

```bash
cd llm-long-term-memory-assistant
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
python3 main.py
```

---

# Roadmap

## Version 1 ✅

* Conversation history
* Keyword-based memory retrieval
* Prompt construction
* Long-term memory storage

## Version 2 🚧

* AI-generated fact extraction
* AI-generated importance scoring
* Persistent memory using JSON

## Version 3

* SQLite memory storage
* Memory editing and deletion
* Memory summarisation

## Version 4

* Embeddings
* Semantic similarity search
* Vector database integration

## Version 5

* Retrieval-Augmented Generation (RAG)
* Hybrid keyword and semantic search
* Production-ready memory architecture

---

# Future Improvements

* Modular project architecture
* Unit testing
* Logging
* Configuration management
* Streaming responses
* Web interface (Streamlit/Gradio)
* Multi-user support

---

# About Me

I'm a Product Leader passionate about building AI-enabled products. Alongside leading product strategy and delivery, I build practical AI projects to deepen my understanding of the engineering behind modern AI systems.

My goal is to combine strong product thinking with technical depth to design, build, and lead world-class AI products.
