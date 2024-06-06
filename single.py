import os
import textract
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from loguru import logger
import hashlib
from prefect import get_run_logger

@task(name="Read PDF", description="Reads the content of a PDF file and returns it as text.", retries=3, retry_delay_seconds=10, timeout_seconds=300)
def read_pdf(file_path: str) -> str:
    logger = get_run_logger()
    try:
        logger.info(f"Reading PDF: {file_path}")
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        logger.error(f"Failed to read PDF {file_path}: {e}")
        raise

@task(name="Chunk Text", description="Chunks the given text into smaller segments of a specified size.", retries=3, retry_delay_seconds=5, timeout_seconds=120)
def chunk_text_generator(text: str, chunk_size: int = 1000) -> list:
    logger = get_run_logger()
    try:
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    except Exception as e:
        logger.error(f"Failed to chunk text: {e}")
        raise

@task(name="Write Chunk", description="Writes a chunk of text to a file.", retries=3, retry_delay_seconds=5, timeout_seconds=60)
def write_chunk(folder: str, filename: str, chunk: str, chunk_index: int):
    logger = get_run_logger()
    try:
        chunk_path = os.path.join(folder, f"{filename}_chunk_{chunk_index}.txt")
        with open(chunk_path, 'w') as f:
            f.write(chunk)
        logger.info(f"Written chunk to {chunk_path}")
    except Exception as e:
        logger.error(f"Failed to write chunk {chunk_index} for file {filename}: {e}")
        raise

@flow(name="Process PDFs", description="Orchestrates the reading, chunking, and writing of PDF files.", task_runner=ConcurrentTaskRunner())
def process_pdfs(pdf_folder: str, output_folder: str):
    logger = get_run_logger()
    try:
        pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
        
        for file_path in pdf_files:
            text = read_pdf(file_path)
            filename = hashlib.md5(file_path.encode()).hexdigest()
            chunks = chunk_text_generator(text)
            for i, chunk in enumerate(chunks):
                write_chunk(output_folder, filename, chunk, i)
    except Exception as e:
        logger.error(f"Failed to process PDFs in folder {pdf_folder}: {e}")
        raise

if __name__ == "__main__":
    pdf_folder = "./data/pdf_folder"
    output_folder = "./data/output_folder"
    os.makedirs(output_folder, exist_ok=True)
    process_pdfs(pdf_folder, output_folder)
