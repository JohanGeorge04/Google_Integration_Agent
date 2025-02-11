from dotenv import load_dotenv
import os
import traceback
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool, AgentType
from lang_folder import create_folder, delete_folder, list_folders_tool, select_folder_tool
from lang_doc import create_doc, update_doc, delete_doc, create_doc_with_content, update_doc_with_content
from langchain.memory import ConversationBufferMemory
from QA import GoogleDocsRetrieverTool

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Gemini API key not found. Please set it in the .env file.")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(google_api_key=gemini_api_key, model="gemini-pro", temperature=0)

# Define tools for document management
doc_tools = [
    Tool(name="CreateDoc", func=create_doc, description="Creates a Google Doc with a title in a specified folder."),
    Tool(name="UpdateDoc", func=update_doc, description="Updates an existing Google Doc with the specified title."),
    Tool(name="CreateDocWithContent", func=create_doc_with_content, description="Creates a Google Doc with a title and content in a specified folder."),
    Tool(name="UpdateDocWithContent", func=update_doc_with_content, description="Updates an existing Google Doc with title and content."),
    Tool(name="DeleteDoc", func=delete_doc, description="Deletes a Google Doc."),
]

folder_tools = [
    Tool(name="ListFolders", func=list_folders_tool, description="Lists all folders in Google Drive."),
    Tool(name="SelectFolder", func=select_folder_tool, description="Selects a folder by name for subsequent operations."),
    Tool(name="CreateFolder", func=create_folder, description="Creates a new folder in Google Drive."),
    Tool(name="DeleteFolder", func=delete_folder, description="Deletes a folder in Google Drive."),
]


retrieval_tool = Tool(
    name="GoogleDocsRetriever",
    func=GoogleDocsRetrieverTool().run,
    description="Retrieves content from Google Docs based on user queries."
)

# Agent manages only document & folder tools
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=doc_tools + folder_tools, 
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "system_message": (
            "You manage Google Drive. "
            "Use available tools to create, update, delete, and list Google Docs & folders. "
            "If no document tool matches the query, return 'No matching tool'."
        )
    }
)


def is_document_query(query):
    """
    Determines if the query is related to document management or retrieval.
    If the query matches document-related tasks, returns True; otherwise, False.
    """
    prompt = (
        "Classify the following user query:\n\n"
        f"Query: \"{query}\"\n\n"
        "Is this query related to document management (creating, updating, deleting, or listing docs/folders)?\n"
        "Respond with 'Yes' for document management, or 'No' for general retrieval queries."
    )

    classification = llm.invoke(prompt).content.strip().lower()
    
    return classification == "yes"


print("Hello! I can help you manage your Google Drive. What would you like to do?")
print("Examples: 'List all folders', 'Create a document', 'Find notes related to AI Research'.")

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    try:
        if is_document_query(user_input):
            response = agent.run(user_input)  
        else:
            response = retrieval_tool.func(user_input) 

        print(f"Assistant: {response}")

    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc()) 
