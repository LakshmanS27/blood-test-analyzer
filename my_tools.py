import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader

@tool("Read blood test report PDF")
def read_data_tool(path: str = 'data/sample.pdf') -> str:
    """Reads and parses a blood test report PDF."""
    try:
        loader = PyPDFLoader(file_path=path)
        pages = loader.load()
        content = "\n".join(page.page_content.strip() for page in pages)
        return content if content else "The PDF is empty."
    except Exception as e:
        return f"Error reading PDF: {e}"

@tool("Analyze nutrition")
def analyze_nutrition_tool(blood_report_data: str) -> str:
    """Analyzes nutrition from the blood test data."""
    return "Nutrition analysis functionality is under development."

@tool("Create exercise plan")
def create_exercise_plan_tool(blood_report_data: str) -> str:
    """Creates an exercise plan based on blood test results."""
    return "Exercise planning functionality is under development."
