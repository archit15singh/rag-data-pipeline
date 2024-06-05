import os
import asyncio
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from aiofiles import open as aio_open
import textract
from loguru import logger
import hashlib

@task
async def read_pdf(file_path: str):
    logger.info(f"Reading PDF: {file_path}")
    text = textract.process(file_path).decode('utf-8')
    return text

@task
async def chunk_text(text: str, chunk_size: int = 1000):
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]

@task
async def write_chunk(folder: str, filename: str, chunk: str, chunk_index: int):
    chunk_path = os.path.join(folder, f"{filename}_chunk_{chunk_index}.txt")
    async with aio_open(chunk_path, 'w') as f:
        await f.write(chunk)
    logger.info(f"Written chunk to {chunk_path}")

@flow(task_runner=ConcurrentTaskRunner())
async def process_pdf(file_path: str, output_folder: str):
    text = await read_pdf.submit(file_path).result()
    filename = hashlib.md5(file_path.encode()).hexdigest()
    tasks = []
    for i, chunk in enumerate(chunk_text(text)):
        tasks.append(write_chunk.submit(output_folder, filename, chunk, i))
    await asyncio.gather(*tasks)

@flow(name="PDF Processing Flow", task_runner=ConcurrentTaskRunner())
async def process_pdfs(pdf_folder: str, output_folder: str):
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    semaphore = asyncio.Semaphore(10)

    async def process_with_semaphore(file_path: str):
        async with semaphore:
            await process_pdf(file_path, output_folder)

    await asyncio.gather(*[process_with_semaphore(f) for f in pdf_files])

if __name__ == "__main__":
    pdf_folder = "./data/pdf_folder"
    output_folder = "./data/output_folder"
    os.makedirs(output_folder, exist_ok=True)
    asyncio.run(process_pdfs(pdf_folder, output_folder))
