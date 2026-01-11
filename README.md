## Introduction : 
---
This POC demonstrates how to:

- Convert natural language questions into SQL using an LLM
- Apply strict guardrails to prevent unsafe or hallucinated queries
- Orchestrate agent behavior deterministically using LangGraph
- Separate responsibilities across intent detection, SQL generation, validation, and execution
- Minimize LLM usage to control cost and rate limits
- Design a database-agnostic system that can later scale to platforms like Snowflake


## Technology Stack

This project is implemented using the following technologies and tools.

---

### Programming Language

- **Python 3.10+**

---

### Agent Orchestration

- **LangGraph**

LangGraph is used to define and manage the agent workflow, including state transitions and execution order.

---

### LLM Integration

- **LangChain**

LangChain is used as the interface layer for interacting with the Large Language Model (LLM).

---

### Large Language Model

- **Google Gemini**

Google Gemini is currently used as the LLM backend for:
- intent classification
- SQL generation from natural-language questions

LLM usage is limited to these stages only.

---

### Database (POC)

- **SQLite**

SQLite is used during the Proof of Concept phase to simulate a relational database.

---

### Database Access & Schema Introspection

- **SQLAlchemy**

SQLAlchemy is used for:
- database connections
- runtime schema introspection
- execution of validated SQL queries

No ORM models are defined.

---

### Configuration Management

- **python-dotenv**

Environment variables are managed using `.env` files and are excluded from version control.

---

### Development Environment

- **Python Virtual Environment (`venv`)**

A virtual environment is used to manage project dependencies.


---
## Setup Instructions

Execute the following commands in order to set up and run the project locally.

```bash
# Clone the repository
git clone https://github.com/SHETTYKSIDDHARTH/DataAgent.git
cd DataAgent

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (macOS / Linux)
# source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Create the local SQLite database
python db/create_db.py

# Create environment variable file
echo GOOGLE_API_KEY=your_api_key_here > .env

# Run the agent
python test_agent.py
```
## Sample Execution & Results

Below are example interactions captured after completing the setup steps.

---
<img width="1920" height="766" alt="image" src="https://github.com/user-attachments/assets/0f330672-a0c2-402a-a563-2342f4be3ba5" />


---
<img width="1648" height="679" alt="image" src="https://github.com/user-attachments/assets/4f1fe494-72e3-462d-8bae-0202b743c64b" />

---

<img width="1645" height="469" alt="image" src="https://github.com/user-attachments/assets/c6add9e8-626c-4114-8017-276a78bd67df" />


