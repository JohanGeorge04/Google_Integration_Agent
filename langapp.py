from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from lang_folder import create_folder, delete_folder, list_folders_tool,select_folder_tool
from lang_doc import create_doc, update_doc, delete_doc
from langchain.memory import ConversationBufferMemory

# Tools with updated descriptions for chat-based interactions
tools = [
    Tool(name="ListFolders", func=list_folders_tool, description="Lists all folders in Google Drive."),
    Tool(name="SelectFolder", func=select_folder_tool, description="Select a folder by name for subsequent operations."),
    Tool(name="CreateDoc", func=create_doc, description="Creates a Google Doc in a specified folder. Specify the title, content, and folder ID."), 
    Tool(name="UpdateDoc", func=update_doc, description="Updates an existing Google Doc. Specify the title and updated content."),
    Tool(name="DeleteDoc", func=delete_doc, description="Deletes a Google Doc. Provide the document title."),
    Tool(name="CreateFolder", func=create_folder, description="Creates a new folder in Google Drive."),
    Tool(name="DeleteFolder", func=delete_folder, description="Deletes a folder in Google Drive. Provide the folder name."),
]

# Initialize the chat-based LLM and agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", memory=memory, verbose=True)

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
