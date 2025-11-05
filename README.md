# 🤖 AI-Powered Email Support for Clothing Store

[![CI Status](https://github.com/ArtemRivnyi/ai-email-support-clothing-store/actions/workflows/main_ci.yml/badge.svg )](https://github.com/ArtemRivnyi/ai-email-support-clothing-store/actions )

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white )
![Ollama](https://img.shields.io/badge/Local%20LLM-Ollama-000000?style=flat-square&logo=ollama&logoColor=white )
![FAISS](https://img.shields.io/badge/Vector%20Search-FAISS-005599?style=flat-square )
![Gmail API](https://img.shields.io/badge/Integration-Gmail%20API-D93025?style=flat-square&logo=gmail&logoColor=white )

[![License](https://img.shields.io/badge/License-MIT-yellow.svg )](https://opensource.org/licenses/MIT )
[![Last Commit](https://img.shields.io/github/last-commit/ArtemRivnyi/ai-email-support-clothing-store?label=Last%20Update&style=flat-square )](https://github.com/ArtemRivnyi/ai-email-support-clothing-store/commits/main )

**AI-Powered Email Support** is an intelligent, automated system designed for e-commerce. Built with **Python**, **Ollama**, and the **Gmail API**, it classifies customer emails, retrieves relevant information from a knowledge base, and generates personalized responses, streamlining customer service workflows.

## 📝 Table of Contents

*   [✨ Features](#-features)
*   [🛠️ Technologies Used](#️-technologies-used)
*   [🚀 Quick Start](#quick-start)
    *   [Prerequisites](#prerequisites)
    *   [Clone the Repository](#clone-the-repository)
    *   [Configure Environment](#configure-environment)
    *   [Run the Application](#run-the-application)
*   [🔧 How It Works](#-how-it-works)
*   [🧠 Customization & Expansion](#-customization--expansion)
*   [📄 License](#-license)
*   [🧰 Maintainer](#-maintainer)

## ✨ Features

*   🧠 **Intelligent Email Classification**: Uses a local LLM (via Ollama) to filter genuine customer inquiries from spam or irrelevant messages.
*   📫 **Automated Gmail Integration**: Fetches unread emails, sends replies, and marks threads as read using the Gmail API.
*   📚 **Dynamic Knowledge Base**: Builds a searchable knowledge base from simple Markdown files, allowing for easy updates and expansion.
*   ⚡ **Efficient Similarity Search**: Leverages **FAISS** and vector embeddings (`all-minilm`) for rapid and accurate retrieval of relevant FAQ answers (RAG).
*   🤖 **Context-Aware Response Generation**: Synthesizes natural, accurate responses using a generative LLM (`gemma:7b`) based only on retrieved knowledge, minimizing hallucinations.
*   🔒 **Local & Scalable**: Runs LLMs locally with Ollama for enhanced data privacy, reduced costs, and easy scalability.

## 🛠️ Technologies Used

The project is built upon a robust stack of modern technologies:

*   **Python**: Version 3.8+ for core application logic.
*   **Ollama**: For running and managing open-source LLMs locally (`gemma:7b`, `all-minilm`).
*   **FAISS**: For efficient, high-speed vector similarity search.
*   **Google Gmail API**: For programmatic email fetching and sending.
*   **Google OAuth**: For secure authentication with Google services.
*   **Docker & Docker Compose**: For containerization and easy deployment.
*   **Markdown**: As the format for the knowledge base files.

## 🚀 Quick Start

Follow these steps to get the AI Email Support system up and running.

### Prerequisites

Ensure you have the following installed and configured:

*   **Python 3.8+**
*   **Git**
*   **Docker** & **Docker Compose**
*   **Ollama**: Install from [ollama.com]() and pull the required models:
    
    ```shell
    ollama pull all-minilm
    ollama pull gemma:7b
    ```
    
*   **Google Cloud Project**:
    1.  Enable the **Gmail API** in the [Google Cloud Console]().
    2.  Configure the **OAuth consent screen** as an "External" user type and add your email as a "Test user".
    3.  Create **OAuth 2.0 Client IDs** for a "Desktop app" and download the `credentials.json` file.

### Clone the Repository

Begin by cloning the project to your local machine:

```shell
git clone https://github.com/ArtemRivnyi/ai-email-support-clothing-store.git
cd ai-email-support-clothing-store
```

### Configure Environment

1.  **Place Credentials**: Move the downloaded `credentials.json` file into the root directory of the project.
    
2.  **Set Environment Variables**: Create a `.env` file in the root directory and add the `client_id` and `client_secret` from your `credentials.json` file:
    
    ```dotenv
    GOOGLE_CLIENT_ID="YOUR_CLIENT_ID_HERE"
    GOOGLE_CLIENT_SECRET="YOUR_CLIENT_SECRET_HERE"
    ```
    
3.  **Install Dependencies**: Create a virtual environment and install the required packages.
    
    ```shell
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # .\venv\Scripts\activate  # On Windows
    pip install -r requirements.txt
    ```
    

### Run the Application

Execute the main script. On the first run, you will be prompted to authenticate with Google.

```shell
python main.py
```

The system will start checking for new emails and processing them automatically. Watch the console for detailed logs.

## 🔧 How It Works

1.  **Fetch Emails**: Periodically scans the Gmail account for unread messages.
2.  **Classify Intent**: Uses `gemma:7b` to determine if an email is a relevant customer inquiry.
3.  **Create Embeddings**: Converts the email content into a vector embedding using `all-minilm`.
4.  **Search Knowledge**: Performs a FAISS similarity search to find the best matching FAQ from the knowledge base.
5.  **Generate Response**: If a match is found, `gemma:7b` crafts a personalized response based on the retrieved information.
6.  **Send and Archive**: The reply is sent, and the original email is marked as read.

## 🧠 Customization & Expansion

*   **Add Knowledge**: Create new `.md` files in the `knowledge_base` directory. The system will automatically index them on restart.
*   **Change Models**: Update the model names in `ollama_utils.py` to use other LLMs supported by Ollama.
*   **Adjust Threshold**: Modify the `SIMILARITY_THRESHOLD` in `main.py` to control response sensitivity.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🧰 Maintainer

**Artem Rivnyi** — Junior Technical Support / DevOps Enthusiast

* 📧 [artemrivnyi@outlook.com](mailto:artemrivnyi@outlook.com)  
* 🔗 [LinkedIn](https://www.linkedin.com/in/artem-rivnyi/)  
* 🌐 [Personal Projects](https://personal-page-devops.onrender.com/)  
* 💻 [GitHub](https://github.com/ArtemRivnyi)
