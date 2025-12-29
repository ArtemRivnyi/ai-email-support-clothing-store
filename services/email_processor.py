import time
from tenacity import retry, stop_after_attempt, wait_exponential
from services.gmail_service import get_gmail_service, send_email_reply, mark_email_as_read
from services.llm_service import classify_email, generate_response_ollama, get_embedding_ollama
from services.rag_service import search_knowledge_base, load_faiss_index, load_indexed_documents
from utils.logger import get_logger
import os

logger = get_logger(__name__)

# Load configuration
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "gemma:7b")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "all-minilm")
FAISS_INDEX_PATH = "embeddings/knowledge_base.index"
DOCUMENTS_PATH = "embeddings/documents.pkl"

class EmailProcessor:
    def __init__(self):
        self.gmail_service = get_gmail_service()
        self.faiss_index = load_faiss_index(FAISS_INDEX_PATH)
        self.indexed_documents = load_indexed_documents(DOCUMENTS_PATH)
        
        if not self.gmail_service:
            logger.error("Failed to initialize Gmail Service")
        if not self.faiss_index or not self.indexed_documents:
            logger.error("Failed to load Knowledge Base")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=4, max=10))
    def process_email(self, email_data):
        """
        Process a single email: Classify -> RAG Search -> Generate Response -> Send Reply
        email_data: dict or EmailMessage object
        """
        email_id = email_data.id
        sender = email_data.sender
        subject = email_data.subject
        text = email_data.text
        thread_id = email_data.thread_id

        logger.info("processing_email", email_id=email_id, sender=sender)

        try:
            # 1. Classify
            is_relevant = classify_email(text, model=OLLAMA_LLM_MODEL)
            if not is_relevant:
                logger.info("email_irrelevant", email_id=email_id)
                mark_email_as_read(self.gmail_service, email_id)
                return

            # 2. RAG Search
            email_embedding = get_embedding_ollama(text, model=OLLAMA_EMBEDDING_MODEL)
            if not email_embedding:
                logger.error("embedding_failed", email_id=email_id)
                return

            matched_document = search_knowledge_base(self.faiss_index, email_embedding, self.indexed_documents)
            
            # 3. Generate Response
            if matched_document:
                logger.info("knowledge_match_found", email_id=email_id, question=matched_document.question)
                answer = generate_response_ollama(text, matched_document.answer, model=OLLAMA_LLM_MODEL)
            else:
                logger.info("no_knowledge_match", email_id=email_id)
                answer = "Спасибо за ваше письмо. Мы получили ваш запрос и постараемся ответить на него как можно скорее."

            # 4. Send Reply
            if answer:
                send_email_reply(self.gmail_service, email_id, sender, subject, answer, thread_id)
                mark_email_as_read(self.gmail_service, email_id)
                logger.info("reply_sent", email_id=email_id)

        except Exception as e:
            logger.error("processing_error", email_id=email_id, error=str(e))
            raise e # Retry will catch this
