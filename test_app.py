import tempfile
import os
import fitz
import pytest

def test_is_pdf_file():
    assert is_pdf_file('document.pdf') == True
    assert is_pdf_file('DOCUMENT.PDF') == True  
    assert is_pdf_file('image.jpg') == False
    assert is_pdf_file('filepdf') == False
    assert is_pdf_file('report.PdF') == True

def is_pdf_file(filename):
    return filename.lower().endswith('.pdf')

def check_pdf_valid(path):
    try:
        with fitz.open(path) as doc:
            return True
    except Exception:
        return False

def test_check_pdf_valid_correct_pdf():
    # Проверяем временный корректный PDF файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), 'Test PDF')
        doc.save(tmp.name)
        doc.close()
        valid = check_pdf_valid(tmp.name)
        assert valid == True
    os.remove(tmp.name)

def test_check_pdf_valid_broken_pdf():
    # Проверяем временный некорректный файл с pdf расширением
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(b"This is not a valid pdf content")
        tmp.close()
        valid = check_pdf_valid(tmp.name)
        assert valid == False
    os.remove(tmp.name)
