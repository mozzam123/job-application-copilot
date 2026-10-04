# Job Application Copilot

A local AI-powered Chrome extension that generates personalized, evidence-backed answers for job application questions based on the job description, candidate profile, and relevant GitHub projects.

The current version is built specifically for **Wellfound** and runs locally using **FastAPI, Ollama, Qwen3, local embeddings, and FAISS**.

## Overview

Job applications often ask questions such as:

> What interests you about working for this company?

> Why are you a good fit for this role?

Writing a meaningful answer for every application requires understanding the company, analyzing the job requirements, and connecting them to relevant experience.

Job Application Copilot automates that process while keeping the final application submission completely under the user's control.

The extension reads the current Wellfound job page, extracts the relevant context, retrieves GitHub projects that semantically match the job requirements, and uses a local LLM to generate a concise and personalized answer.

## How It Works

```text
Wellfound Job Page
        ↓
Chrome Extension
        ↓
Wellfound Page Extractor
        ↓
Job Description + Requirements
        ↓
Semantic Search over GitHub Projects
        ↓
Top Relevant Project Evidence
        ↓
Candidate Profile
        +
GitHub Project Evidence
        +
Job Context
        +
Application Question
        ↓
Prompt Builder
        ↓
Local Qwen3 LLM
        ↓
Personalized Answer
        ↓
Copy & Paste
```

## GitHub Project RAG

Instead of relying only on a static list of skills, the application uses the candidate's actual GitHub projects as technical evidence.

Selected GitHub repository READMEs are fetched and converted into embeddings using a local embedding model.

The embeddings are stored in a FAISS vector index.

When a job description is processed, the application performs semantic retrieval against this project knowledge base and selects the most relevant projects.

For example, if a job requires:

```text
AI Agents
LangChain
LangGraph
Tool Calling
Human-in-the-Loop
```

the system may retrieve projects involving:

```text
Multi-Agent Architecture
Supervisor / Worker Agents
LangGraph
Tool Calling
Parallel Execution
Human-in-the-Loop
Agent Guardrails
```

The LLM can then generate an answer based on actual project evidence instead of simply claiming familiarity with the technologies.

GitHub projects are treated as **hands-on project experience**, not professional employment experience.

## Features

- Chrome Extension using Manifest V3
- Wellfound job page extraction
- Job title extraction
- Company information extraction
- Job description extraction
- Requirements extraction
- FastAPI backend
- Local LLM generation with Ollama
- Qwen3 support
- Provider-based LLM architecture
- Structured candidate profile
- GitHub README ingestion
- Local embeddings
- FAISS vector search
- Semantic project retrieval
- Evidence-backed answer generation
- Anti-hallucination prompt rules
- Natural and concise application answers
- Manual Copy Answer workflow
- No automatic job submission
- Fully local AI pipeline

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- HTTPX

### AI

- Ollama
- Qwen3:8B
- `nomic-embed-text`
- Retrieval-Augmented Generation (RAG)

### Vector Search

- FAISS
- NumPy

### Browser Extension

- JavaScript
- HTML/CSS
- Chrome Extension Manifest V3

### Data Source

- GitHub project READMEs

## Project Structure

```text
job-application-copilot/
│
├── backend/
│   │
│   ├── app/
│   │   ├── knowledge/
│   │   │   ├── __init__.py
│   │   │   ├── project_sources.py
│   │   │   └── project_index.py
│   │   │
│   │   ├── llm/
│   │   │   ├── base.py
│   │   │   └── ollama.py
│   │   │
│   │   ├── candidate_profile.py
│   │   ├── models.py
│   │   ├── prompt_builder.py
│   │   └── main.py
│   │
│   ├── data/
│   │   └── project_index/
│   │       ├── projects.faiss
│   │       └── metadata.json
│   │
│   ├── scripts/
│   │   └── build_project_index.py
│   │
│   └── requirements.txt
│
└── extension/
    ├── extractors/
    │   └── wellfound.js
    ├── content.js
    ├── manifest.json
    ├── popup.html
    └── popup.js
```

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mozzam123/job-application-copilot.git
cd job-application-copilot
```

### 2. Create a Virtual Environment

```bash
cd backend

python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama Models

Install the generation model:

```bash
ollama pull qwen3:8b
```

Install the embedding model:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

### 5. Build the GitHub Project Knowledge Base

```bash
python scripts/build_project_index.py
```

This fetches the configured GitHub project READMEs, generates local embeddings, and creates the FAISS project index.

Re-run this command whenever relevant GitHub projects or their READMEs are updated.

### 6. Start the Backend

```bash
uvicorn app.main:app --reload
```

The API will run locally on:

```text
http://127.0.0.1:8000
```

### 7. Load the Chrome Extension

Open:

```text
chrome://extensions
```

Then:

1. Enable **Developer Mode**
2. Select **Load unpacked**
3. Select the `extension/` directory

## Usage

1. Start Ollama.
2. Start the FastAPI backend.
3. Open a job listing on Wellfound.
4. Open the Job Application Copilot extension.
5. Enter the application question.
6. Click **Generate Answer**.
7. Review the generated answer.
8. Click **Copy Answer**.
9. Paste it into the application.

The extension does **not** automatically submit applications.

## Grounding and Hallucination Prevention

Generated answers are constrained to information supported by:

- Candidate profile
- GitHub project READMEs
- Retrieved project evidence
- Current job context

The prompt explicitly prevents the model from:

- Inventing technologies
- Inventing employers
- Inventing years of experience
- Inventing achievements or metrics
- Treating GitHub projects as professional employment
- Claiming experience simply because a technology appears in the job description

This allows answers to remain confident while still being grounded in actual experience.

## Current Limitations

The current version intentionally keeps the architecture simple.

- Wellfound is the only supported job platform.
- Application questions must be entered manually.
- Candidate information is currently stored in `candidate_profile.py`.
- GitHub projects must currently be configured for indexing.
- The project index must be manually rebuilt when projects change.
- Retrieval currently operates primarily at the project README level.
- The local FastAPI backend and Ollama must be running while using the extension.

## Future Improvements

### Resume-Based Candidate Profile

Allow users to upload a resume and automatically extract structured information such as:

- Professional experience
- Skills
- Technologies
- Education
- Projects

This would replace or dynamically generate the current static `candidate_profile.py`.

### Automatic GitHub Repository Discovery

Connect to a GitHub profile and automatically discover suitable repositories instead of manually maintaining the repository list.

The system should distinguish meaningful portfolio projects from test, utility, forked, or unrelated repositories.

### Automatic Project Index Refresh

Detect updated or newly created GitHub projects and incrementally update the vector index instead of manually running:

```bash
python scripts/build_project_index.py
```

### README Chunking

Split large project READMEs into smaller semantic chunks.

Instead of:

```text
1 project → 1 embedding
```

support:

```text
1 project
   ↓
Architecture chunk
Technology chunk
Features chunk
Implementation chunk
   ↓
Multiple embeddings
```

This should improve retrieval precision for larger projects.

### Retrieval Quality Improvements

Add:

- Similarity thresholds
- Duplicate evidence filtering
- Requirement-aware retrieval
- Metadata filtering
- Hybrid keyword + semantic retrieval
- Reranking

### Requirement Extraction

Use an LLM or structured parser to first extract the important technical requirements from the job description.

```text
Full Job Description
        ↓
Requirement Extraction
        ↓
Python
LangGraph
AI Agents
REST APIs
System Design
        ↓
Project Retrieval
```

This would prevent irrelevant parts of long job descriptions from influencing semantic search.

### Evidence Ranking

Rank evidence based on strength:

```text
Professional Experience
        ↓
Strongest Evidence

Hands-on GitHub Project
        ↓
Strong Evidence

Technical Knowledge
        ↓
Supporting Evidence
```

The generation model could use this ranking when deciding how confidently to phrase a claim.

### Automatic Question Detection

Detect application questions directly from the Wellfound page instead of requiring the user to manually paste or type them.

### Additional Job Platforms

Create platform-specific extractors for:

- LinkedIn
- Indeed
- Other job portals

while keeping the backend and generation pipeline platform-independent.

### Configurable LLM Providers

Extend the existing provider abstraction to support:

- Ollama
- Groq
- OpenAI
- Anthropic
- Other compatible providers

without changing the main application logic.

### Answer Editing

Allow users to:

- Regenerate
- Shorten
- Make more technical
- Make more conversational
- Change tone

before copying the final answer.

### Local User Configuration

Move candidate profile, GitHub username, selected repositories, models, and generation preferences into configuration instead of hardcoded Python files.

### Extension UX Improvements

Improve the popup with:

- Detected company and role preview
- Retrieved project preview
- Loading states
- Regenerate button
- Answer history
- Editable generated answer
- Settings

## Design Principles

This project intentionally follows a few principles:

**Grounded over generic**  
Answers should be backed by actual candidate experience.

**Evidence over keywords**  
Having a technology in a skills list is less valuable than showing where it was actually used.

**Local-first**  
The core AI pipeline can run without paid LLM APIs.

**Human-controlled**  
The system assists with applications but does not automatically submit them.

**Simple before complex**  
More advanced retrieval, automation, and agentic workflows should only be added when they provide a clear improvement.

## Status

**V1 Complete**

The current version supports the complete workflow:

```text
Wellfound
→ Job Extraction
→ GitHub Project Retrieval
→ Candidate Context
→ Local LLM
→ Personalized Answer
→ Manual Copy
```

Further development will focus on improving retrieval quality, automating candidate/project data management, supporting additional platforms, and improving the extension experience.
