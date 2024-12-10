from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langcreate import create_doc,update_doc,delete_doc



tools = [
    Tool(name="CreateDoc", func=create_doc, description="Creates a document."),
    Tool(name="UpdateDoc", func=update_doc, description="Updates a document ."),
    Tool(name="DeleteDoc", func=delete_doc, description="Deletes a document ."),
]

llm = ChatOpenAI(model="gpt-4", temperature=0)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


response = agent.run("Create a document with Title: My Notes, Content: This is a sample document.")
print(response)

