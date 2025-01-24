from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from lang_folder import create_folder, delete_folder, list_folders_tool, select_folder_tool
from lang_doc import create_doc, update_doc, delete_doc,create_doc_with_content,update_doc_with_content
from langchain.memory import ConversationBufferMemory

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")


llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0)


folder_tools = [
    Tool(name="ListFolders", func=list_folders_tool, description="Lists all folders in Google Drive."),
    Tool(name="SelectFolder", func=select_folder_tool, description="Select a folder by name for subsequent operations."),
    Tool(name="CreateFolder", func=create_folder, description="Creates a new folder in Google Drive."),
    Tool(name="DeleteFolder", func=delete_folder, description="Deletes a folder in Google Drive."),
]


doc_tools = [
    Tool(name="CreateDoc", func=create_doc, description="Creates a Google Doc with title in a specified folder."),
    Tool(name="UpdateDoc", func=update_doc, description="Updates an existing Google Doc with secified title."),
    Tool(name="CreateDocWithContent", func=create_doc_with_content, description="Creates a Google Doc with a title and content in a specified folder."),
    Tool(name="UpdateDocWithContent", func=update_doc_with_content, description="Updates an existing Google Doc with title and content."),
    Tool(name="DeleteDoc", func=delete_doc, description="Deletes a Google Doc."),]

tools = folder_tools + doc_tools

# Initialize conversation memory
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize agent with additional control instructions
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={"system_message": "You are a helpful assistant that manages Google Drive. Please follow the user's instructions carefully and confirm actions before executing."}
)

print("Hello! I can help you manage your Google Drive. What would you like to do?")
print("Examples: 'List all folders', 'Create a document', 'Delete a folder', etc.")

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break
    try:
        response = agent.run(user_input)
        print(f"Assistant: {response}")
    except Exception as e:
        print(f"Error: {e}")
        print("An error occurred. Please try again.")
