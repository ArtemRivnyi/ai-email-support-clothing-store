import os
import tempfile
import pytest
from faiss_utils import (
    parse_knowledge_base_file,
    load_knowledge_base,
    build_and_save_faiss_index,
    load_faiss_index,
    load_indexed_documents,
    search_knowledge_base,
    KnowledgeDocument,
)
import numpy as np

# Мокаем get_embedding_ollama внутри ollama_utils
import sys
sys.modules['ollama_utils'] = __import__('types').SimpleNamespace(
    get_embedding_ollama=lambda text, model: [0.1 * i for i in range(128)]
)

@pytest.fixture
def sample_md_file():
    content = """
# Вопрос
Как оформить возврат?

# Ответ
Вы можете вернуть товар в течение 14 дней с момента получения заказа.

# Ключевые слова
возврат, возврат товара, политика
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode='w', encoding='utf-8')
    tmp.write(content)
    tmp.close()
    yield tmp.name
    os.remove(tmp.name)

def test_parse_knowledge_base_file(sample_md_file):
    doc = parse_knowledge_base_file(sample_md_file)
    assert isinstance(doc, KnowledgeDocument)
    assert "возврат" in doc.question.lower()
    assert "14 дней" in doc.answer

def test_load_knowledge_base(sample_md_file):
    dir_path = os.path.dirname(sample_md_file)
    docs = load_knowledge_base(dir_path)
    assert len(docs) > 0
    assert all(isinstance(d, KnowledgeDocument) for d in docs)

def test_build_and_load_faiss_index(sample_md_file):
    docs = load_knowledge_base(os.path.dirname(sample_md_file))
    index_path = tempfile.NamedTemporaryFile(delete=False).name
    docs_path = tempfile.NamedTemporaryFile(delete=False).name

    index = build_and_save_faiss_index(
        docs, embedding_model="all-minilm", dimension=128,
        index_path=index_path, documents_path=docs_path
    )
    assert index is not None
    loaded_index = load_faiss_index(index_path)
    assert loaded_index.ntotal == len(docs)

    loaded_docs = load_indexed_documents(docs_path)
    assert len(loaded_docs) == len(docs)

    os.remove(index_path)
    os.remove(docs_path)

def test_search_knowledge_base(sample_md_file):
    docs = load_knowledge_base(os.path.dirname(sample_md_file))
    index = build_and_save_faiss_index(docs, "all-minilm", 128, "faiss.idx", "docs.pkl")
    query = [0.1 * i for i in range(128)]
    result = search_knowledge_base(index, query, docs)
    assert result is not None
    assert isinstance(result, KnowledgeDocument)
    os.remove("faiss.idx")
    os.remove("docs.pkl")
