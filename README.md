# Google API Integration with LangChain

This repository demonstrates a seamless integration of Google API services with LangChain to enhance the functionalities of AI-powered applications. By leveraging the power of Google APIs, this project allows efficient storage, retrieval, and management of meeting notes and other project-related data.

## Features

- **Google API Integration**: Enables connection with Google services for storing and retrieving meeting notes.
- **LangChain Support**: Utilizes LangChain for natural language processing and understanding.
- **Efficient Workflow**: Automates the management of meeting notes to boost productivity.
- **Team Collaboration**: Facilitates collaborative management of project data.

## Getting Started

### Prerequisites

Before setting up the project, ensure you have the following:

- Python 3.8 or later
- A Google Cloud account
- Google API credentials (OAuth 2.0 client ID)
- Required Python libraries:
  - `langchain`
  - `google-api-python-client`
  - `oauth2client`
  - `openai`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/google-integration-langchain.git
   cd google-integration-langchain
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google API credentials:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the required Google APIs (e.g., Google Drive, Google Docs, etc.).
   - Download the OAuth 2.0 client ID JSON file and save it in the project directory.
   - Rename the file to `credentials.json`.
   ```

### Usage

1. Authenticate with Google API:
   ```bash
   python authenticate.py
   ```
   Follow the instructions to complete the authentication process.

2. Run the main script:
   ```bash
   python langapp.py
   ```

## Project Structure

```
.
├── credentials.json          # Google API credentials file
├── langapp.py                # Main script for the integration
├── credentials.py            # Authentication handler for Google API
├── doc_manage.py             # Document management utilities
├── folder_manage.py          # Folder management utilities
├── lang_doc.py               # LangChain document-related utilities
├── lang_folder.py            # LangChain folder-related utilities
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
```

## Contributing

We welcome contributions to improve this integration. Feel free to fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [LangChain Documentation](https://langchain.readthedocs.io/)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [OpenAI](https://openai.com/)

