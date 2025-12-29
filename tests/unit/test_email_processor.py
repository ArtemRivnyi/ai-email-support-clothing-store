import unittest
from unittest.mock import MagicMock, patch
from services.email_processor import EmailProcessor
from services.gmail_service import EmailMessage

class TestEmailProcessor(unittest.TestCase):
    @patch('services.email_processor.get_gmail_service')
    @patch('services.email_processor.load_faiss_index')
    @patch('services.email_processor.load_indexed_documents')
    def setUp(self, mock_load_docs, mock_load_index, mock_get_service):
        self.processor = EmailProcessor()
        self.mock_gmail = mock_get_service.return_value

    @patch('services.email_processor.classify_email')
    @patch('services.email_processor.mark_email_as_read')
    def test_process_irrelevant_email(self, mock_mark_read, mock_classify):
        # Setup
        mock_classify.return_value = False
        email = EmailMessage('1', 'sender@test.com', 'me', 'Spam', 'Buy crypto', 't1')
        
        # Execute
        self.processor.process_email(email)
        
        # Verify
        mock_classify.assert_called_once()
        mock_mark_read.assert_called_with(self.processor.gmail_service, '1')

    @patch('services.email_processor.classify_email')
    @patch('services.email_processor.get_embedding_ollama')
    @patch('services.email_processor.search_knowledge_base')
    @patch('services.email_processor.generate_response_ollama')
    @patch('services.email_processor.send_email_reply')
    @patch('services.email_processor.mark_email_as_read')
    def test_process_relevant_email_success(self, mock_mark_read, mock_send, mock_gen, mock_search, mock_embed, mock_classify):
        # Setup
        mock_classify.return_value = True
        mock_embed.return_value = [0.1, 0.2]
        mock_search.return_value = MagicMock(question="Q", answer="A")
        mock_gen.return_value = "Generated Answer"
        
        email = EmailMessage('2', 'client@test.com', 'me', 'Help', 'Where is my order?', 't2')
        
        # Execute
        self.processor.process_email(email)
        
        # Verify
        mock_send.assert_called_with(self.processor.gmail_service, '2', 'client@test.com', 'Help', 'Generated Answer', 't2')
        mock_mark_read.assert_called_with(self.processor.gmail_service, '2')

if __name__ == '__main__':
    unittest.main()
