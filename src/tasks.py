# src/tasks.py
from prefect import task, get_run_logger
import os
import json
import textract
import requests
from markdownify import markdownify as md

@task(retries=3, retry_delay_seconds=10)
def read_pdf(file_path: str):
    logger = get_run_logger()
    try:
        text = textract.process(file_path).decode('utf-8')
        logger.info(f"Read PDF from {file_path} (length: {len(text)} characters)")
        return text
    except Exception as e:
        logger.error(f"Failed to read PDF from {file_path}: {str(e)}")
        raise

@task(retries=3, retry_delay_seconds=10)
def chunk_text(text: str, chunk_size: int = 100):
    logger = get_run_logger()
    try:
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        logger.info(f"Chunked text into {len(chunks)} chunks")
        return chunks
    except Exception as e:
        logger.error(f"Failed to chunk text: {str(e)}")
        raise

@task(retries=3, retry_delay_seconds=10)
def write_json(data, output_path: str):
    logger = get_run_logger()
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f)
        logger.info(f"Wrote JSON to {output_path}")
    except Exception as e:
        logger.error(f"Failed to write JSON to {output_path}: {str(e)}")
        raise

@task(retries=3, retry_delay_seconds=10)
def read_html(file_path: str):
    logger = get_run_logger()
    try:
        with open(file_path, 'r') as file:
            html_content = file.read()
        logger.info(f"Read HTML from {file_path} (length: {len(html_content)} characters)")
        return html_content
    except Exception as e:
        logger.error(f"Failed to read HTML from {file_path}: {str(e)}")
        raise

@task(retries=3, retry_delay_seconds=10)
def convert_html_to_markdown(html_content: str):
    logger = get_run_logger()
    try:
        markdown_content = md(html_content)
        logger.info(f"Converted HTML to Markdown (length: {len(markdown_content)} characters)")
        return markdown_content
    except Exception as e:
        logger.error(f"Failed to convert HTML to Markdown: {str(e)}")
        raise

@task(retries=3, retry_delay_seconds=10)
def write_file(content: str, output_path: str):
    logger = get_run_logger()
    try:
        with open(output_path, 'w') as f:
            f.write(content)
        logger.info(f"Wrote content to {output_path}")
    except Exception as e:
        logger.error(f"Failed to write content to {output_path}: {str(e)}")
        raise

@task(retries=3, retry_delay_seconds=10)
def call_api(file_name: str):
    logger = get_run_logger()
    try:
        # Simulating an API call
        response = {"file_name": file_name, "status": "processed"}
        logger.info(f"Called API with {file_name} (response: {response})")
        return response
    except Exception as e:
        logger.error(f"Failed to call API with {file_name}: {str(e)}")
        raise
