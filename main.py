# main.py
import os
import time
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Импортируем утилиты
# Важно: KnowledgeDocument теперь импортируется из faiss_utils
from gmail_utils import get_gmail_service, get_new_emails, send_email_reply, mark_email_as_read, EmailMessage
from ollama_utils import classify_email, generate_response_ollama, get_embedding_ollama
from faiss_utils import load_knowledge_base, build_and_save_faiss_index, load_faiss_index, search_knowledge_base, load_indexed_documents, check_index_and_documents_match, KnowledgeDocument

def main():
    load_dotenv() # Загружаем переменные окружения из .env

    # --- Настройки из .env ---
    # Теперь мы ИСПРАВЛЕННО получаем значения из .env
    ollama_llm_model = os.getenv("OLLAMA_LLM_MODEL", "gemma:7b") # Модель для LLM, по умолчанию gemma:7b
    ollama_embedding_model = os.getenv("OLLAMA_EMBEDDING_MODEL", "all-minilm") # Модель для эмбеддингов, по умолчанию all-minilm
    check_interval_minutes = int(os.getenv("CHECK_INTERVAL_MINUTES", 5)) # Интервал проверки, по умолчанию 5 минут

    knowledge_base_dir = "knowledge_base"
    faiss_index_path = "embeddings/knowledge_base.index"
    documents_path = "embeddings/documents.pkl" # Путь для сохранения списка документов

    logging.info("Запуск системы поддержки по электронной почте на базе ИИ...")

    # 1. Инициализация сервиса Gmail API
    gmail_service = get_gmail_service()
    if not gmail_service:
        logging.error("Не удалось инициализировать сервис Gmail API. Выход.")
        return

    # 2. Настройка FAISS индекса
    faiss_index = None
    indexed_knowledge_documents = [] # Список документов, которые фактически проиндексированы

    # Сначала загружаем "сырые" документы из markdown файлов
    raw_knowledge_documents = load_knowledge_base(knowledge_base_dir)
    
    if not raw_knowledge_documents:
        logging.error("В базе знаний не найдено документов. Невозможно построить/загрузить FAISS индекс. Выход.")
        return

    # Проверяем, существует ли индекс FAISS и соответствует ли он текущей базе знаний
    if check_index_and_documents_match(faiss_index_path, documents_path, len(raw_knowledge_documents)):
        faiss_index = load_faiss_index(faiss_index_path)
        indexed_knowledge_documents = load_indexed_documents(documents_path)
        logging.info("FAISS индекс и документы успешно загружены.")
    else:
        logging.info("FAISS индекс не найден или устарел/не соответствует. Строим новый.")
        
        # Получаем эмбеддинг для первого документа для определения размерности
        logging.info("Получаем эмбеддинг для первого документа для определения размерности...")
        sample_content_for_embedding = f"Вопрос: {raw_knowledge_documents[0].question}\nОтвет: {raw_knowledge_documents[0].answer}"
        sample_embedding = get_embedding_ollama(sample_content_for_embedding, ollama_embedding_model)
        
        if sample_embedding:
            dimension = len(sample_embedding)
            logging.info(f"Размерность эмбеддинга: {dimension}")
            faiss_index = build_and_save_faiss_index(
                raw_knowledge_documents, ollama_embedding_model, dimension, faiss_index_path, documents_path
            )
            # После построения индекса, нужно заново загрузить документы, которые были сохранены с индексом
            if faiss_index:
                indexed_knowledge_documents = load_indexed_documents(documents_path)
        else:
            logging.error("Не удалось получить образец эмбеддинга. Невозможно построить FAISS индекс. Выход.")
            return

    if faiss_index is None or not indexed_knowledge_documents:
        logging.error("Не удалось настроить FAISS индекс или загрузить проиндексированные документы. Выход.")
        return

    # Основной цикл для периодической проверки электронной почты
    logging.info("Система поддержки по электронной почте на базе ИИ запущена и готова к работе.")
    while True:
        logging.info("\nПроверяем новые непрочитанные письма...")
        emails = get_new_emails(gmail_service, query='is:unread')

        if not emails:
            logging.info("Новых непрочитанных писем не найдено.")
        else:
            for email in emails:
                logging.info(f"\n--- Обработка письма от: {email.sender}, Тема: {email.subject[:50]}...")

                # Проверка на noreply
                if "noreply" in email.sender.lower():
                    logging.info(f"Письмо от {email.sender} содержит 'noreply'. Игнорируем.")
                    mark_email_as_read(gmail_service, email.id)
                    continue

                # 5. Классификация письма
                logging.info("Классифицируем письмо...")
                # Используем ollama_llm_model из .env
                is_relevant = classify_email(email.text, model=ollama_llm_model)

                if not is_relevant:
                    logging.info("Письмо классифицировано как не относящееся к поддержке клиентов. Помечаем как прочитанное и пропускаем.")
                    mark_email_as_read(gmail_service, email.id)
                    continue

                logging.info("Письмо классифицировано как релевантное.")

                # 6. Поиск в базе знаний (FAISS)
                logging.info("Генерируем эмбеддинг письма для поиска...")
                # Используем ollama_embedding_model из .env
                email_embedding = get_embedding_ollama(email.text, model=ollama_embedding_model)

                if email_embedding is not None:
                    logging.info("Ищем наилучшее совпадение в базе знаний...")
                    # Передаем проиндексированные документы в search_knowledge_base
                    matched_document = search_knowledge_base(faiss_index, email_embedding, indexed_knowledge_documents)

                    if matched_document:
                        logging.info(f"Найдена релевантная информация в базе знаний (Вопрос: {matched_document.question[:50]}...)")
                        # 7. Генерация ответа
                        logging.info("Генерируем ответ с помощью LLM...")
                        # Используем ollama_llm_model из .env
                        generated_answer = generate_response_ollama(email.text, matched_document.answer, model=ollama_llm_model)
                        
                        if generated_answer:
                            logging.info(f"Предпросмотр сгенерированного ответа: {generated_answer[:200]}...")
                            # 8. Отправка ответа
                            logging.info(f"Отправляем ответ на {email.sender}...")
                            send_email_reply(gmail_service, email.id, email.sender, email.subject, generated_answer, email.thread_id)
                            mark_email_as_read(gmail_service, email.id)
                            logging.info("Ответ отправлен, и письмо помечено как прочитанное.")
                        else:
                            logging.warning("Не удалось сгенерировать ответ на основе найденной информации.")
                            # Если LLM не сгенерировала ответ, можно отправить запасной ответ или оставить непрочитанным.
                            fallback_answer_llm_fail = "Извините, мы не смогли сгенерировать полный ответ на ваш запрос. Наши специалисты свяжутся с вами в ближайшее время."
                            logging.info(f"Отправляем запасной ответ (ошибка LLM) и помечаем письмо как прочитанное: {fallback_answer_llm_fail[:100]}")
                            send_email_reply(gmail_service, email.id, email.sender, email.subject, fallback_answer_llm_fail, email.thread_id)
                            mark_email_as_read(gmail_service, email.id)
                    else:
                        logging.info("В базе знаний не найдено достаточно релевантной информации для этого письма (порог сходства не пройден).")
                        # 9. Отправка запасного ответа (fallback)
                        fallback_answer_no_match = "Спасибо за ваше письмо. Мы получили ваш запрос и постараемся ответить на него как можно скорее. Если вопрос срочный, пожалуйста, свяжитесь с нами по телефону."
                        logging.info(f"Отправляем запасной ответ (нет совпадений в БД) и помечаем письмо как прочитанное: {fallback_answer_no_match[:100]}")
                        send_email_reply(gmail_service, email.id, email.sender, email.subject, fallback_answer_no_match, email.thread_id)
                        mark_email_as_read(gmail_service, email.id)
                else:
                    logging.warning("Не удалось сгенерировать эмбеддинг для письма. Невозможно выполнить поиск в базе знаний.")
                    # Запасной ответ в случае ошибки генерации эмбеддинга
                    fallback_answer_embed_fail = "Извините, мы столкнулись с технической проблемой при обработке вашего запроса. Пожалуйста, попробуйте еще раз позже или свяжитесь с нами другим способом."
                    logging.info(f"Отправляем запасной ответ (ошибка эмбеддинга) и помечаем письмо как прочитанное: {fallback_answer_embed_fail[:100]}")
                    send_email_reply(gmail_service, email.id, email.sender, email.subject, fallback_answer_embed_fail, email.thread_id)
                    mark_email_as_read(gmail_service, email.id)

        # Ждем некоторое время перед следующей проверкой
        logging.info(f"\nОжидание {check_interval_minutes} минут до следующей проверки...")
        time.sleep(check_interval_minutes * 60)

if __name__ == "__main__":
    main()