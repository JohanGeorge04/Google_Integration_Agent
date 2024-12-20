from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langcreate import create_doc,update_doc,delete_doc
from lang_folder import create_folder, delete_folder 



tools = [
    Tool(name="CreateDoc", func=create_doc, description="Creates a document."),
    Tool(name="UpdateDoc", func=update_doc, description="Updates a document ."),
    Tool(name="DeleteDoc", func=delete_doc, description="Deletes a document ."),
    Tool(name="CreateFolder", func=create_folder, description="Creates a folder in Google Drive."),
    Tool(name="DeleteFolder", func=delete_folder, description="Deletes a folder in Google Drive."),
]

llm = ChatOpenAI(model="gpt-4", temperature=0)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# response = agent.run("Create document with title sample with content this is a sample ")
# response = agent.run("update document with title sample with content this is a new sample ")
# response = agent.run("Delete document with title sample")
# response = agent.run("Create folder with folder name Test Document ")
# response = agent.run("Delete folder with folder name Test Document ")


