from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langcreate import create_and_store_doc_tool

tools = [
    Tool(
        name="Create and Store Document",
        func=create_and_store_doc_tool,
        description="Use this tool to create and store Google Docs."
    )
]

llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


response = agent.run("Create a document with the text 'Hello, world!'")
print(response)

