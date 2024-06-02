## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

### Load environment variables
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

from crewai import Agent

from tools import search_tool, BloodTestReportTool

### Loading LLM from Google AI
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash',
                             temperature=0.5,
                             verbose=True,
                             google_api_key=os.getenv('GOOGLE_API_KEY'))

# Creating an Experienced Doctor agent
doctor=Agent(
    role="Senior Experienced Doctor",
    goal="Deliver advice to patients based on their query\n query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "Driven by passion, you are a senior doctor."
        "Since most of your patients come from non-medical backgrounds, you explain things to them in a casual and kind manner."
        "Your speciality is finding abnormalities in the blood test report."
        "You are knowledeable in analyzing the blood test report, summarizing it in an easy-to-understand manner if the patient asks."
        "You can also provide health recommendations in detail to your patients along with web url links to support your points."
    ),
    tools=[search_tool, BloodTestReportTool().read_data_tool],
    llm=llm,
    max_iter=10,
    max_rpm=14,
    allow_delegation=False
)

# Creatinga a verifier agent
verifier = Agent(
    role="Blood Report Verifier",
    goal="Only read the data once.\n\
You will be provided with a path to the file given by the user, read the data of the file provided by the user and use your knowledge to verify if the data is a blood report or not.\n\
If it is a blood test report then tell the doctor that the data is correct.\
If it's not the blood report and tell the senior doctor that no blood report was given.\n\
file_path: {file_path}.\n\
After getting the blood test report you should tell the doctor that it is a valid report.",
    verbose=True,
    memory=True,
    backstory=(
        "You have experience with understanding a blood report in any format"
        "You always read the blood report and then pass it to the senior doctor after verifying it."
    ),
    tools = [BloodTestReportTool().read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=7,
    allow_delegation=True
)

