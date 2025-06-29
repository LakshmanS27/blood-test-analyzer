import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_community.chat_models import ChatLiteLLM  # ✅ use LiteLLM wrapper
from my_tools import read_data_tool, analyze_nutrition_tool, create_exercise_plan_tool

# ✅ Ensure MISTRAL_API_KEY is set
if not os.getenv("MISTRAL_API_KEY"):
    raise ValueError("MISTRAL_API_KEY not set in .env")

llm = ChatLiteLLM(
    model="mistral/mistral-medium-latest",  # ✅ LiteLLM expects provider/model format
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.7
)

doctor = Agent(
    role="Experienced Medical Doctor",
    goal="Provide evidence-based medical insights from the uploaded blood test report.",
    verbose=True,
    memory=True,
    backstory="Board-certified internal medicine specialist with 20+ years of diagnostic experience.",
    tools=[read_data_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

verifier = Agent(
    role="Medical File Verifier",
    goal="Ensure the uploaded document is a valid and readable blood test report.",
    verbose=True,
    memory=True,
    backstory="You specialize in analyzing medical records for completeness and authenticity.",
    tools=[read_data_tool],
    llm=llm,
    max_iter=1,
    allow_delegation=False
)

nutritionist = Agent(
    role="Clinical Nutrition Expert",
    goal="Provide dietary advice based on identified deficiencies in the blood report.",
    verbose=True,
    memory=True,
    backstory="Licensed dietitian skilled in interpreting blood chemistry for nutritional optimization.",
    tools=[read_data_tool, analyze_nutrition_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

exercise_specialist = Agent(
    role="Rehabilitation and Fitness Advisor",
    goal="Suggest suitable exercises based on health indicators in the report.",
    verbose=True,
    memory=True,
    backstory="Certified personal trainer with a focus on clinical and post-injury fitness programming.",
    tools=[read_data_tool, create_exercise_plan_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)
