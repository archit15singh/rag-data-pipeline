# RAG Data Pipeline

The project is designed to process and transform various types of documents, including PDFs and HTML files, into different formats such as JSON and Markdown. This pipeline uses Prefect for orchestration.

## Pipelines
- **PDF to JSON Conversion:** Reads PDFs, chunks the text, and writes it to a JSON file.
- **HTML to Markdown Conversion:** Reads HTML files, converts them to Markdown, and writes the output to a file.
- **PDF to API and JSON Conversion:** Reads PDFs, sends them to an API, and writes the API response to a JSON file.

Each step in the data processing pipeline is encapsulated as a Prefect task, for modularity and reusability. The pipeline is defined using YAML configuration files, which specify the flow and dependencies of tasks.

## Installation

To get started with the RAG Data Pipeline, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone git@github.com:archit15singh/rag-data-pipeline.git
   cd rag-data-pipeline
   ```

2. **Set up a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

### Running the Pipelines

To run the individual pipelines, use the `main.py` script.

1. **Run Individual Pipelines:**
   ```bash
   python src/main.py
   ```

   This will execute all individual pipelines defined in the `main.py` script.

### YAML Configuration

The YAML configuration files define the flow of tasks and their dependencies. Below is an example of a pipeline configuration:

```yaml
flow_name: Pipeline
parameters:
  - name: pdf_path
    default: /path/to/your/file.pdf
  - name: html_path
    default: /path/to/your/file.html
  - name: json_output_path
    default: /path/to/output/file.json
  - name: markdown_output_path
    default: /path/to/output/file.md
  - name: api_response_output_path
    default: /path/to/output/response.json
tasks:
  - name: read_pdf
    params:
      file_path: pdf_path
  - name: chunk_text
    params:
      text: read_pdf
    depends_on: read_pdf
  - name: write_json
    params:
      data: chunk_text
      output_path: json_output_path
    depends_on: chunk_text
  - name: read_html
    params:
      file_path: html_path
  - name: convert_html_to_markdown
    params:
      html_content: read_html
    depends_on: read_html
    parallel: true
  - name: write_file
    params:
      content: convert_html_to_markdown
      output_path: markdown_output_path
    depends_on: convert_html_to_markdown
  - name: call_api
    params:
      file_name: pdf_path
    depends_on: read_pdf
    parallel: true
  - name: write_api_response
    params:
      data: call_api
      output_path: api_response_output_path
    depends_on: call_api
```

## Task Details

### read_pdf

Reads a PDF file and extracts the text.

### chunk_text

Chunks the extracted text into smaller pieces.

### write_json

Writes the chunked text into a JSON file.

### read_html

Reads an HTML file and extracts its content.

### convert_html_to_markdown

Converts HTML content to Markdown format.

### write_file

Writes the converted Markdown content to a file.

### call_api

Simulates an API call with the PDF file.

### write_api_response

Writes the API response to a JSON file.

## Error Handling

The pipeline uses Prefect's built-in retry mechanisms to handle transient errors. Each task can be configured with a number of retries and a delay between retries.

Example:

```python
@task(retries=3, retry_delay_seconds=10)
def read_pdf(file_path: str):
    # Task implementation
```

