import pytest
from main import BooksCollector

# Создаем новый объект BooksCollector перед каждым тестом
@pytest.fixture   
def collector():
    return BooksCollector()