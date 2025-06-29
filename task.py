from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist
from my_tools import read_data_tool

help_patients = Task(
    description="Analyze the uploaded blood test report and provide medical insights.",
    expected_output="Medical summary of report findings with actionable next steps or concerns.",
    agent=doctor,
    tools=[read_data_tool],
    async_execution=False
)

nutrition_analysis = Task(
    description="Analyze nutrition indicators from the blood report and provide dietary suggestions.",
    expected_output="List of nutrients to improve, suggested foods, and lifestyle recommendations.",
    agent=nutritionist,
    tools=[read_data_tool],
    async_execution=False
)

exercise_planning = Task(
    description="Generate a basic exercise plan based on overall blood report and fitness indicators.",
    expected_output="Weekly exercise routine adapted to user’s health status.",
    agent=exercise_specialist,
    tools=[read_data_tool],
    async_execution=False
)

verification = Task(
    description="Check if the uploaded file is a valid blood test report.",
    expected_output="True/False status and key format details of the document.",
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False
)
