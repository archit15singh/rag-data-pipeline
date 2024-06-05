import os
import textract
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from loguru import logger
import hashlib
import datetime

@task(retries=3, retry_delay=datetime.timedelta(seconds=10), timeout_seconds=300)
def read_pdf(file_path: str) -> str:
    try:
        logger.info(f"Reading PDF: {file_path}")
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        logger.error(f"Failed to read PDF {file_path}: {e}")
        raise

@task(retries=3, retry_delay=datetime.timedelta(seconds=5), timeout_seconds=120)
def chunk_text(text: str, chunk_size: int = 1000) -> list:
    try:
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    except Exception as e:
        logger.error(f"Failed to chunk text: {e}")
        raise

@task(retries=3, retry_delay=datetime.timedelta(seconds=5), timeout_seconds=60)
def write_chunk(folder: str, filename: str, chunk: str, chunk_index: int):
    try:
        chunk_path = os.path.join(folder, f"{filename}_chunk_{chunk_index}.txt")
        with open(chunk_path, 'w') as f:
            f.write(chunk)
        logger.info(f"Written chunk to {chunk_path}")
    except Exception as e:
        logger.error(f"Failed to write chunk {chunk_index} for file {filename}: {e}")
        raise

@flow(name="Process Single PDF", description="Orchestrates the reading, chunking, and writing of a single PDF file.", task_runner=ConcurrentTaskRunner())
def process_pdf(file_path: str, output_folder: str):
    try:
        text = read_pdf(file_path)
        chunks = chunk_text(text)
        filename = hashlib.md5(file_path.encode()).hexdigest()
        for i, chunk in enumerate(chunks):
            write_chunk(output_folder, filename, chunk, i)
    except Exception as e:
        logger.error(f"Failed to process PDF {file_path}: {e}")
        raise

@flow(name="Process Multiple PDFs", description="Processes all PDFs in the specified folder.", task_runner=ConcurrentTaskRunner())
def process_pdfs(pdf_folder: str, output_folder: str):
    try:
        pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
        for file_path in pdf_files:
            process_pdf(file_path, output_folder)
    except Exception as e:
        logger.error(f"Failed to process PDFs in folder {pdf_folder}: {e}")
        raise

if __name__ == "__main__":
    pdf_folder = "./data/pdf_folder"
    output_folder = "./data/output_folder"
    os.makedirs(output_folder, exist_ok=True)
    process_pdfs(pdf_folder, output_folder)
