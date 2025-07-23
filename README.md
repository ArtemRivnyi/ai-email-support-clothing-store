# AI-Powered Email Support System for Online Clothing Store

[![GitHub last commit](https://img.shields.io/github/last-commit/artemRivnyi/ai-email-support-clothing-store)](https://github.com/artemRivnyi/ai-email-support-clothing-store/commits/main)
[![GitHub top language](https://img.shields.io/github/languages/top/artemRivnyi/ai-email-support-clothing-store)](https://github.com/artemRivnyi/ai-email-support-clothing-store)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project is an intelligent automated email support system designed for an online clothing store. It leverages Large Language Models (LLMs) and vector databases to classify incoming customer emails, find relevant answers from a structured knowledge base, and generate personalized responses. The system aims to streamline customer service operations by automating responses to frequently asked questions (FAQs), allowing human agents to focus on more complex or nuanced inquiries.

## Key Features

* **Email Processing & Management:** Seamlessly connects with Gmail API to fetch unread customer emails, send automated replies, and mark processed emails as read. This ensures a clean and efficient inbox workflow.
* **Intelligent Email Classification:** Utilizes a locally-run Large Language Model (LLM) via Ollama (`gemma:7b` with a fine-tuned prompt) to accurately determine if an incoming email is a genuine customer support inquiry relevant to the online clothing store's domain (e.g., orders, delivery, returns, sizing, product availability, website issues). This crucial step filters out spam, marketing, or unrelated inquiries (like tech support or restaurant bookings) with high precision.
* **Dynamic Knowledge Base:**
    * **Markdown-based FAQs:** The knowledge base is built from easily editable Markdown (`.md`) files stored in the `knowledge_base/` directory. Each FAQ entry is structured with distinct "Question", "Answer", and "Keywords" sections.
    * **Automated Indexing:** The system automatically parses these Markdown files, extracts the relevant content, and processes it into a searchable format.
* **Efficient Similarity Search (RAG):**
    * **Vector Embeddings:** Transforms both the incoming email content and the FAQ entries into high-dimensional numerical vectors (embeddings) using the `all-minilm` model via Ollama.
    * **FAISS Integration:** Employs FAISS (Facebook AI Similarity Search) to create and utilize an optimized vector index. This allows for lightning-fast retrieval of the most semantically similar FAQ entry to the customer's query.
    * **Adjustable Similarity Threshold:** A configurable threshold ensures that only highly relevant answers are considered, preventing the system from responding with inaccurate information.
* **Context-Aware Response Generation:** Leverages Ollama (e.g., `gemma:7b`) to synthesize a natural, polite, and comprehensive reply. The LLM's prompt is specifically engineered to generate answers based *only* on the retrieved knowledge base information and the original customer email, minimizing "hallucinations" and ensuring factual accuracy within the store's context.
* **Scalability & Local Control:** By using Ollama, the project can run LLMs locally, offering greater control over data privacy and potentially reducing API costs, while allowing easy scalability by adding more FAQ documents.

## Technologies Used

* **Python 3.x:** The core programming language.
* **Ollama:** A powerful tool for running and managing open-source Large Language Models locally.
    * `all-minilm`: Used for generating highly effective text embeddings.
    * `gemma:7b` (or similar): Used for intelligent email classification and generating human-like responses.
* **FAISS (Facebook AI Similarity Search):** An efficient library for similarity search and clustering of dense vectors, enabling fast retrieval from the knowledge base.
* **Google Gmail API:** Facilitates programmatic interaction with Gmail accounts for email operations.
* **`google-auth-oauthlib`, `google-api-python-client`:** Python client libraries for Google APIs, handling OAuth 2.0 authorization.
* **`python-dotenv`:** For secure management of environment variables (e.g., API keys).
* **Markdown:** Used as a simple, human-readable format for the knowledge base.
* **`requests` & `json`:** For direct HTTP communication with the Ollama API endpoint.
* **`logging`:** For comprehensive logging and debugging throughout the system.

## Project Structure
Отлично! У вас уже есть GitHub аккаунт, и вы создали .gitignore. Это ускоряет процесс.



Markdown

# AI-Powered Email Support System for Online Clothing Store

[![GitHub last commit](https://img.shields.io/github/last-commit/artemRivnyi/ai-email-support-clothing-store)](https://github.com/artemRivnyi/ai-email-support-clothing-store/commits/main)
[![GitHub top language](https://img.shields.io/github/languages/top/artemRivnyi/ai-email-support-clothing-store)](https://github.com/artemRivnyi/ai-email-support-clothing-store)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project is an intelligent automated email support system designed for an online clothing store. It leverages Large Language Models (LLMs) and vector databases to classify incoming customer emails, find relevant answers from a structured knowledge base, and generate personalized responses. The system aims to streamline customer service operations by automating responses to frequently asked questions (FAQs), allowing human agents to focus on more complex or nuanced inquiries.

## Key Features

* **Email Processing & Management:** Seamlessly connects with Gmail API to fetch unread customer emails, send automated replies, and mark processed emails as read. This ensures a clean and efficient inbox workflow.
* **Intelligent Email Classification:** Utilizes a locally-run Large Language Model (LLM) via Ollama (`gemma:7b` with a fine-tuned prompt) to accurately determine if an incoming email is a genuine customer support inquiry relevant to the online clothing store's domain (e.g., orders, delivery, returns, sizing, product availability, website issues). This crucial step filters out spam, marketing, or unrelated inquiries (like tech support or restaurant bookings) with high precision.
* **Dynamic Knowledge Base:**
    * **Markdown-based FAQs:** The knowledge base is built from easily editable Markdown (`.md`) files stored in the `knowledge_base/` directory. Each FAQ entry is structured with distinct "Question", "Answer", and "Keywords" sections.
    * **Automated Indexing:** The system automatically parses these Markdown files, extracts the relevant content, and processes it into a searchable format.
* **Efficient Similarity Search (RAG):**
    * **Vector Embeddings:** Transforms both the incoming email content and the FAQ entries into high-dimensional numerical vectors (embeddings) using the `all-minilm` model via Ollama.
    * **FAISS Integration:** Employs FAISS (Facebook AI Similarity Search) to create and utilize an optimized vector index. This allows for lightning-fast retrieval of the most semantically similar FAQ entry to the customer's query.
    * **Adjustable Similarity Threshold:** A configurable threshold ensures that only highly relevant answers are considered, preventing the system from responding with inaccurate information.
* **Context-Aware Response Generation:** Leverages Ollama (e.g., `gemma:7b`) to synthesize a natural, polite, and comprehensive reply. The LLM's prompt is specifically engineered to generate answers based *only* on the retrieved knowledge base information and the original customer email, minimizing "hallucinations" and ensuring factual accuracy within the store's context.
* **Scalability & Local Control:** By using Ollama, the project can run LLMs locally, offering greater control over data privacy and potentially reducing API costs, while allowing easy scalability by adding more FAQ documents.

## Technologies Used

* **Python 3.x:** The core programming language.
* **Ollama:** A powerful tool for running and managing open-source Large Language Models locally.
    * `all-minilm`: Used for generating highly effective text embeddings.
    * `gemma:7b` (or similar): Used for intelligent email classification and generating human-like responses.
* **FAISS (Facebook AI Similarity Search):** An efficient library for similarity search and clustering of dense vectors, enabling fast retrieval from the knowledge base.
* **Google Gmail API:** Facilitates programmatic interaction with Gmail accounts for email operations.
* **`google-auth-oauthlib`, `google-api-python-client`:** Python client libraries for Google APIs, handling OAuth 2.0 authorization.
* **`python-dotenv`:** For secure management of environment variables (e.g., API keys).
* **Markdown:** Used as a simple, human-readable format for the knowledge base.
* **`requests` & `json`:** For direct HTTP communication with the Ollama API endpoint.
* **`logging`:** For comprehensive logging and debugging throughout the system.

## Project Structure

.
├── main.py                     # Main execution loop, coordinating all system modules.
├── gmail_utils.py              # Handles all Gmail API interactions: authentication, fetching, sending, and marking emails.
├── faiss_utils.py              # Manages the FAISS vector index, parses markdown knowledge base files, and performs similarity searches.
├── ollama_utils.py             # Integrates with Ollama for LLM tasks: generating embeddings, classifying emails, and creating responses.
├── .env                        # Environment variables (e.g., Google API credentials - excluded from Git by .gitignore for security).
├── .gitignore                  # Specifies files and directories to be excluded from Git version control.
├── README.md                   # Project documentation (this file).
└── knowledge_base/             # Directory containing the Frequently Asked Questions (FAQ) in Markdown format.
├── faq_1_password_reset.md # Example FAQ file for password recovery.
├── faq_2_delivery_times.md # Example FAQ file for delivery times.
├── faq_3_returns_policy.md # Example FAQ file for returns policy.
├── faq_4_order_status.md   # Example FAQ file for order status.
├── faq_5_payment_methods.md# Example FAQ file for payment methods.
├── faq_6_size_chart.md     # Example FAQ file for size chart information.
└── ... (Additional FAQ files can be added here following the specified format)

## Setup and Installation

### Prerequisites

Before running the application, ensure you have the following installed and configured:

1.  **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/).
2.  **Git**: Download from [git-scm.com](https://git-scm.com/downloads).
3.  **Ollama Installation**:
    * Download and install Ollama from the official website: [ollama.com](https://ollama.com/).
    * After installation, pull the required LLM models using your terminal:
        ```bash
        ollama pull all-minilm
        ollama pull gemma:7b # Or choose another compatible generative model like 'llama2'
        ```
    * Verify that the Ollama server is running (it usually starts automatically).
4.  **Google Cloud Project & Gmail API Credentials**:
    * Go to the [Google Cloud Console](https://console.cloud.google.com/).
    * Create a new Google Cloud Project.
    * Navigate to **APIs & Services > Library** and enable the **Gmail API**.
    * Go to **APIs & Services > OAuth consent screen**:
        * Set **User type** to `External`.
        * Configure the consent screen details (App name, support email, developer contact information).
        * **Crucially, add the Google email address you plan to use for the bot to the "Test users" section.** This allows your application to access that specific email account during development without needing full verification.
    * Go to **APIs & Services > Credentials**:
        * Click `+ CREATE CREDENTIALS` and select **OAuth client ID**.
        * Choose **Desktop app** as the Application type.
        * Download the `credentials.json` file.
        * Open this downloaded `credentials.json` file. You will find your `client_id` and `client_secret` within it.

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/artemRivnyi/ai-email-support-clothing-store.git](https://github.com/artemRivnyi/ai-email-support-clothing-store.git)
    cd ai-email-support-clothing-store
    ```

2.  **Create a virtual environment (highly recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *If `requirements.txt` is missing, you can create it by running `pip freeze > requirements.txt` or manually adding the following to a new `requirements.txt` file:*
    ```
    google-api-python-client
    google-auth-oauthlib
    python-dotenv
    ollama # The official Ollama Python client library
    faiss-cpu # Or faiss-gpu if you have a compatible NVIDIA GPU and CUDA setup
    numpy
    ```

4.  **Set up environment variables:**
    * Create a new file named `.env` in the root directory of your project (where `main.py` is located).
    * Add your Google API `client_id` and `client_secret` to this file:
        ```env
        GOOGLE_CLIENT_ID="YOUR_CLIENT_ID_FROM_GOOGLE_CLOUD_CONSOLE"
        GOOGLE_CLIENT_SECRET="YOUR_CLIENT_SECRET_FROM_GOOGLE_CLOUD_CONSOLE"
        ```
    * **Important:** This `.env` file is listed in `.gitignore` and **will not be committed to your GitHub repository**, ensuring your sensitive credentials remain private.

5.  **Prepare the Knowledge Base:**
    * Ensure your `.md` FAQ files are placed inside the `knowledge_base/` directory.
    * Each file **must** contain sections for `# Вопрос`, `# Ответ`, and `# Ключевые слова` (note the space after `#`). Example:
        ```markdown
        # Вопрос
        Как я могу отследить свой заказ?

        # Ответ
        Вы можете отслеживать статус вашего заказа, войдя в свой личный кабинет на нашем сайте. ...

        # Ключевые слова
        отследить, заказ, статус, доставка, где мой заказ
        ```

## Running the System

1.  **Ensure the Ollama server is actively running** in the background (check your system tray or run `ollama serve` in a dedicated terminal window).
2.  **Run the main script from your project's root directory:**
    ```bash
    python main.py
    ```
3.  **Initial Gmail API Authorization (First Run):**
    * The very first time you execute `main.py`, a web browser window will automatically open. This is for you to authorize your application's access to Gmail.
    * Follow the prompts, log in with the Google account you added as a "Test user" in the Google Cloud Console.
    * **Crucially, carefully review and grant ALL requested permissions** (specifically `gmail.readonly`, `gmail.send`, `gmail.modify` scope).
    * Upon successful authorization, a `token.pickle` file will be created in your project's root directory. This file stores your authentication tokens, allowing subsequent runs to bypass the browser authorization step.
    * **Troubleshooting `Insufficient Permissions`:** If you ever modify the `SCOPES` in `gmail_utils.py` or encounter "Insufficient Permissions" errors, you **must delete the `token.pickle` file** and re-run `main.py` to trigger a fresh re-authorization with the updated permissions.

The system will now begin its operation, periodically checking your inbox for unread emails. All processing steps, including classification, search, response generation, and email actions, will be logged to your console.

## Customization and Further Development

* **LLM Model Selection:** Experiment with different Ollama models (e.g., `llama2`, `mistral`, `codellama`) by modifying the `model` parameters in `ollama_utils.py` to find the best balance of performance and accuracy for your needs.
* **Similarity Threshold Tuning:** Adjust the `SIMILARITY_THRESHOLD` value in `faiss_utils.py`. This parameter directly influences how "close" an email's query must be to a knowledge base entry for an automated answer to be generated. Fine-tune this based on observed accuracy.
* **Prompt Engineering:** The prompts within `ollama_utils.py` for `classify_email` and `generate_response_ollama` are critical for the system's performance. Continuous refinement of these prompts can significantly enhance classification precision and the quality of generated responses.
* **Email Filtering & Queries:** The `query` parameter in `get_new_emails` within `gmail_utils.py` can be modified to implement more sophisticated email filtering logic (e.g., specific labels, senders, or keywords).
* **Error Handling & Fallbacks:** Implement more robust error handling for external API calls and add more sophisticated fallback mechanisms (e.g., forwarding unanswerable emails to a human agent, notifying administrators).
* **Additional Features:** Consider integrating with customer relationship management (CRM) systems, adding sentiment analysis, or incorporating multilingual support.

## Author

www.linkedin.com/in/artem-rivnyi

---