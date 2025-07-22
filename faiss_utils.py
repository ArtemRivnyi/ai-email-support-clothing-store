# faiss_utils.py
import faiss
import numpy as np
import os
import pickle # Для сохранения/загрузки списка документов
import glob # Для поиска файлов в директории
import logging # Для более информативного вывода
from typing import List, Optional

# Настройка логирования для этого модуля
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Класс для хранения документов базы знаний (убедитесь, что он совпадает с вашей версией в main.py)
class KnowledgeDocument:
    def __init__(self, question: str, answer: str, keywords: str, source_file: str):
        self.question = question
        self.answer = answer
        self.keywords = keywords
        self.source_file = source_file # Имя файла-источника для отладки

    def __repr__(self):
        return f"KnowledgeDocument(Q: {self.question[:30]}..., A: {self.answer[:30]}..., File: {self.source_file})"

def parse_knowledge_base_file(filepath: str) -> Optional[KnowledgeDocument]:
    """
    Парсит один Markdown файл базы знаний.
    Ожидает разделы # Вопрос, # Ответ, # Ключевые слова.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        question = ""
        answer = ""
        keywords = ""
        current_section = None

        lines = content.split('\n')
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith('# Вопрос'):
                current_section = "question"
                question = "" # Сбрасываем содержимое, если секция найдена
            elif line_stripped.startswith('# Ответ'):
                current_section = "answer"
                answer = ""
            elif line_stripped.startswith('# Ключевые слова'):
                current_section = "keywords"
                keywords = ""
            elif current_section == "question":
                question += line + "\n" # Добавляем всю строку, чтобы сохранить форматирование/абзацы
            elif current_section == "answer":
                answer += line + "\n"
            elif current_section == "keywords":
                keywords += line + "\n"
        
        # Удаляем лишние пробелы и символы новой строки в конце
        question = question.strip()
        answer = answer.strip()
        keywords = keywords.strip()

        if not question or not answer:
            logging.warning(f"Пропускаем файл {filepath} из-за отсутствия разделов 'Вопрос' или 'Ответ'.")
            return None
        
        return KnowledgeDocument(question=question, answer=answer, keywords=keywords, source_file=os.path.basename(filepath))
    except Exception as e:
        logging.error(f"Ошибка при парсинге файла {filepath}: {e}")
        return None

def load_knowledge_base(directory: str) -> List[KnowledgeDocument]:
    """
    Загружает все Markdown файлы из указанной директории в базу знаний.
    """
    documents = []
    if not os.path.isdir(directory):
        logging.warning(f"Директория базы знаний не найдена: {directory}")
        return documents

    md_files = glob.glob(os.path.join(directory, "*.md"))
    if not md_files:
        logging.warning(f"В директории {directory} не найдено файлов Markdown (*.md).")
        return documents

    for filepath in md_files:
        doc = parse_knowledge_base_file(filepath)
        if doc:
            documents.append(doc)
    logging.info(f"Загружено {len(documents)} документов из базы знаний.")
    return documents

def build_and_save_faiss_index(documents: List[KnowledgeDocument], embedding_model: str, dimension: int, index_path: str, documents_path: str) -> Optional[faiss.Index]:
    """
    Строит FAISS индекс из эмбеддингов документов и сохраняет его вместе с документами.
    """
    # Импортируем get_embedding_ollama здесь, чтобы избежать циклической зависимости
    # и чтобы ollama_utils мог быть импортирован без faiss_utils
    from ollama_utils import get_embedding_ollama

    if not documents:
        logging.warning("Нет документов для построения FAISS индекса.")
        return None

    logging.info("Строим эмбеддинги базы знаний...")
    embeddings = []
    indexed_documents = [] # Сохраняем документы, для которых успешно получен эмбеддинг

    for i, doc in enumerate(documents):
        # Используем вопрос + ответ для эмбеддинга
        content_for_embedding = f"Вопрос: {doc.question}\nОтвет: {doc.answer}"
        emb = get_embedding_ollama(content_for_embedding, embedding_model)
        if emb is not None: # Проверяем, что эмбеддинг получен успешно (не None)
            embeddings.append(emb)
            indexed_documents.append(doc)
        else:
            logging.error(f"Не удалось получить эмбеддинг для документа из {doc.source_file}. Пропускаем.")
            # Если эмбеддинг не получен, это может быть проблемой, поэтому
            # можно прекратить построение индекса или продолжить с оставшимися.
            # Для надежности - пока логируем ошибку, но продолжаем, если есть другие эмбеддинги.

    if not embeddings:
        logging.error("Не удалось получить ни одного эмбеддинга для построения индекса.")
        return None

    embeddings_array = np.array(embeddings).astype('float32')
    
    # Инициализация FAISS индекса
    index = faiss.IndexFlatL2(dimension) # L2 расстояние
    index.add(embeddings_array)

    # Создаем директорию для сохранения, если ее нет
    os.makedirs(os.path.dirname(index_path), exist_ok=True)

    # Сохранение индекса и списка документов (indexed_documents)
    try:
        faiss.write_index(index, index_path)
        with open(documents_path, 'wb') as f:
            pickle.dump(indexed_documents, f) # Сохраняем только те документы, которые были проиндексированы
        logging.info(f"FAISS индекс построен и сохранен в {index_path}")
        logging.info(f"Документы базы знаний сохранены в {documents_path}")
        return index
    except Exception as e:
        logging.error(f"Ошибка при сохранении FAISS индекса или документов: {e}")
        return None

def load_faiss_index(index_path: str) -> Optional[faiss.Index]:
    """
    Загружает ранее построенный FAISS индекс.
    """
    if not os.path.exists(index_path):
        logging.info(f"FAISS индекс не найден по пути {index_path}")
        return None
    try:
        index = faiss.read_index(index_path)
        logging.info(f"FAISS индекс загружен из {index_path}")
        return index
    except Exception as e:
        logging.error(f"Ошибка при загрузке FAISS индекса из {index_path}: {e}")
        return None

def load_indexed_documents(documents_path: str) -> List[KnowledgeDocument]:
    """
    Загружает список документов, которые были использованы для построения FAISS индекса.
    """
    if not os.path.exists(documents_path):
        logging.warning(f"Файл документов {documents_path} не найден.")
        return []
    try:
        with open(documents_path, 'rb') as f:
            documents = pickle.load(f)
        logging.info(f"Загружено {len(documents)} документов из {documents_path}.")
        return documents
    except Exception as e:
        logging.error(f"Ошибка при загрузке документов из {documents_path}: {e}")
        return []

def check_index_and_documents_match(index_path: str, documents_path: str, current_raw_doc_count: int) -> bool:
    """
    Проверяет, соответствует ли существующий FAISS индекс и сохраненные документы
    текущему количеству документов в базе знаний.
    """
    if not os.path.exists(index_path) or not os.path.exists(documents_path):
        logging.info("FAISS индекс или файл документов не найдены.")
        return False
    try:
        index = faiss.read_index(index_path)
        with open(documents_path, 'rb') as f:
            indexed_documents = pickle.load(f)
        
        # Мы сравниваем количество элементов в индексе и в списке проиндексированных документов
        # с количеством документов, которые были успешно загружены из markdown файлов.
        # В идеале все 3 счетчика должны совпадать.
        if index.ntotal == len(indexed_documents) and index.ntotal == current_raw_doc_count:
            logging.info(f"FAISS индекс ({index.ntotal}), сохраненные документы ({len(indexed_documents)}) и текущая база знаний ({current_raw_doc_count}) соответствуют.")
            return True
        else:
            logging.warning(f"FAISS индекс ({index.ntotal}) или сохраненные документы ({len(indexed_documents)}) не соответствуют текущей базе знаний ({current_raw_doc_count}). Индекс будет перестроен.")
            return False
    except Exception as e:
        logging.error(f"Ошибка при проверке FAISS индекса и документов: {e}. Индекс будет перестроен.")
        return False

def search_knowledge_base(index: faiss.Index, query_embedding: List[float], documents: List[KnowledgeDocument], k: int = 1) -> Optional[KnowledgeDocument]:
    """
    Ищет в FAISS индексе наиболее похожий документ.
    Возвращает KnowledgeDocument, если совпадение достаточно хорошее, иначе None.
    """
    if index is None:
        logging.error("FAISS индекс не загружен. Невозможно выполнить поиск.")
        return None

    query_vector = np.array([query_embedding]).astype('float32')
    distances, indices = index.search(query_vector, k)

    # --- КРИТИЧНОЕ ДОБАВЛЕНИЕ: ПОРОГ СХОДСТВА ---
    # Для all-minilm:latest (который вы используете для эмбеддингов), L2 расстояние.
    # Меньшее значение = более высокое сходство.
    # 0.8 - хорошее стартовое значение, но его нужно будет настроить.
    SIMILARITY_THRESHOLD = 5.0 # ЭКСПЕРИМЕНТИРУЙТЕ С ЭТИМ ЗНАЧЕНИЕМ!

    if indices.size > 0 and indices[0][0] != -1:
        best_match_index = indices[0][0]
        best_match_distance = distances[0][0] # Получаем фактическое расстояние
        
        logging.info(f"Найдено наилучшее совпадение (индекс: {best_match_index}, расстояние L2: {best_match_distance:.4f})")

        if best_match_distance < SIMILARITY_THRESHOLD:
            if 0 <= best_match_index < len(documents):
                return documents[best_match_index]
            else:
                logging.warning(f"Найденный индекс {best_match_index} вне диапазона списка документов. Возможно, список документов устарел.")
                return None
        else:
            logging.info(f"Наилучшее совпадение слишком далеко (расстояние L2: {best_match_distance:.4f} >= порога {SIMILARITY_THRESHOLD}).")
            return None # Совпадение не найдено, так как расстояние слишком велико
    else:
        logging.info("В FAISS индексе не найдено соответствующего документа.")
        return None