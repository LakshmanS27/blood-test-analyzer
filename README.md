# 🧪 Blood Test Report Analyzer (CrewAI + FastAPI + Celery + Mistral AI)

This is a scalable AI system for analyzing blood test PDF reports using [CrewAI](https://github.com/joaomdmoura/crewai), Celery, and FastAPI. The system uses multiple AI agents (doctor, nutritionist, exercise specialist, verifier) to collaboratively analyze and summarize blood reports. Tasks are executed asynchronously using Celery and results are stored in a local SQLite database.

---

## 🚀 Features

- 🧠 AI-driven analysis of PDF blood reports (via Mistral LLM + CrewAI agents)
- 🔄 Asynchronous task processing with **Celery** + **Redis** via **Docker**
- 🗃️ Result storage using **SQLite** and **SQLAlchemy**
- 📁 Modular architecture (Agents / Tasks / Tools separated)
- ⚙️ Built-in input validation, cleanup, and error handling
- 🐳 Redis runs via Docker for easy setup on any platform

---

## 📦 Tech Stack

| Layer       | Technology                    |
|------------ |-------------------------------|
| Backend API | FastAPI                        |
| LLM Agent   | CrewAI + LiteLLM (Mistral)     |
| Task Queue  | Celery with Redis              |
| Database    | SQLite via SQLAlchemy          |
| Deployment  | Localhost + Docker Redis       |

---

## 📸 API Endpoints

### `POST /analyze`

Upload your blood test report (PDF only).

#### Request

- **file**: PDF upload (required)
- **query**: Text prompt (optional)

#### Response

```json
{
  "status": "processing",
  "task_id": "xxxx-xxxx-xxxx",
  "message": "Analysis in progress. Poll /result/{task_id} to get the report."
}
```

---

### `GET /result/{task_id}`

Fetch analysis result once processing completes.

#### Response

```json
{
  "status": "completed",
  "result": "Your blood report analysis..."
}
```

---

## 🐛 Bugs Found & 🔧 Fixes Applied

### `main.py`

| Issue                         | Fix                                      |
|------------------------------|------------------------------------------|
| ❌ `Crew.kickoff()` misused   | ✅ Used `crew.kickoff(inputs={...})`     |
| ❌ `file_path` unused         | ✅ Passed into `kickoff()` properly      |
| ❌ No file validation         | ✅ `.pdf` check added                    |
| ❌ Blocking sync inside async | ✅ Used Celery `.delay()`                |
| ❌ Unsafe cleanup             | ✅ Added `os.path.exists()` before delete|

---

### `agents.py`

| Issue                             | Fix                                  |
|----------------------------------|--------------------------------------|
| ❌ `llm = llm` caused NameError   | ✅ Defined `llm` using `ChatLiteLLM` |
| ❌ Used `tool=` instead of `tools=` | ✅ Fixed keyword                    |
| ❌ Agents unrealistic              | ✅ Made roles clinically accurate    |

---

### `task.py`

| Issue                      | Fix                                           |
|---------------------------|-----------------------------------------------|
| ❌ Joke/placeholder logic  | ✅ Rewritten with real clinical goals         |
| ❌ All tasks use wrong agent | ✅ Correct agents assigned                  |
| ❌ Tool used as class attr | ✅ Replaced with top-level `read_data_tool()`|

---

### `my_tools.py`

| Issue                                   | Fix                                      |
|----------------------------------------|------------------------------------------|
| ❌ `PyPDFLoader` not imported           | ✅ Fixed import                           |
| ❌ `read_data_tool()` async & incorrect | ✅ Rewritten as proper sync tool function|
| ❌ Unused stub tools                    | ✅ Added placeholders and mapped to agents|

---

### `celery_worker.py`

| Issue                    | Fix                                       |
|--------------------------|-------------------------------------------|
| ❌ Not modular            | ✅ Separated task logic into Celery task  |
| ❌ No result storage      | ✅ Uses SQLite to persist output          |
| ❌ No cleanup on failure  | ✅ File removed safely with fallback      |

---

## ⚙️ Setup Instructions

1. **Clone the Repo**

```bash
git clone https://github.com/your-username/blood-test-analyzer.git
cd blood-test-analyzer
```

2. **Create Virtual Environment**

```bash
python -m venv venv_311
venv_311\Scriptsctivate  # On Windows
# OR
source venv_311/bin/activate  # On macOS/Linux
```

3. **Install Requirements**

```bash
pip install -r requirements.txt
```

4. **Start Redis via Docker**

```bash
docker run -d -p 6379:6379 redis
```

5. **Start Celery Worker**

```bash
celery -A celery_worker.celery_app worker --loglevel=info --pool=solo
```

6. **Run FastAPI Server**

```bash
uvicorn main:app --reload
```

7. **Open API in Browser**

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Folder Structure

```
.
├── main.py               # FastAPI application
├── celery_worker.py      # Celery app definition
├── celery_tasks.py       # Celery task logic
├── agents.py             # CrewAI agents
├── task.py               # Task definitions per agent
├── my_tools.py           # PDF reader and data extract tools
├── database.py           # DB session & connection logic
├── models.py             # ORM model for result storage
├── data/                 # Uploaded PDFs stored temporarily
└── reports.db            # SQLite database for results
```

---

## 📬 License

MIT License. Use responsibly.
