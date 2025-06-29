from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os, uuid
from celery_tasks import process_blood_report
from celery.result import AsyncResult
from celery_worker import celery_app
from database import init_db

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        query = query.strip() or "Summarise my Blood Test Report"

        # Submit job to Celery
        task = process_blood_report.delay(query, file_path)

        return {
            "status": "processing",
            "task_id": task.id,
            "message": "Analysis in progress. Poll /result/{task_id} to get the report."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")

@app.get("/result/{task_id}")
def get_result(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    if task.state == "PENDING":
        return {
            "status": "pending",
            "message": "The task is still being processed."
        }

    elif task.state == "SUCCESS":
        return {
            "status": "completed",
            "result": task.result
        }

    elif task.state == "FAILURE":
        return {
            "status": "failed",
            "error": str(task.result)
        }

    return {"status": task.state}

# Initialize DB on app startup
init_db()
