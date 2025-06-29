from celery import shared_task
import os
import traceback

from crewai import Crew, Process
from agents import doctor
from task import help_patients
from database import SessionLocal
from models import ReportResult

@shared_task(bind=True)
def process_blood_report(self, query: str, file_path: str):
    task_id = self.request.id
    db = SessionLocal()

    try:
        # Step 1: Run CrewAI
        crew = Crew(
            agents=[doctor],
            tasks=[help_patients],
            process=Process.sequential,
            verbose=True
        )
        result = crew.kickoff(inputs={"query": query, "file_path": file_path})
        result_text = str(result)

        # Step 2: Save result to DB
        db.add(ReportResult(
            task_id=task_id,
            filename=os.path.basename(file_path),
            query=query,
            result=result_text
        ))
        db.commit()
        return result_text

    except Exception as e:
        error_msg = f"Error during processing:\n{traceback.format_exc()}"
        db.add(ReportResult(
            task_id=task_id,
            filename=os.path.basename(file_path),
            query=query,
            result=error_msg
        ))
        db.commit()
        return error_msg

    finally:
        db.close()
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass
