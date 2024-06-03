from flow_builder import create_flow_from_yaml

def main():
    # Example: Running Pipeline 1
    flow1 = create_flow_from_yaml('flows/pipeline1.yaml')
    flow1(pdf_path='/workspaces/rag-data-pipeline/data/1.pdf', json_output_path='/workspaces/rag-data-pipeline/data/1.json')

    # Example: Running Pipeline 2
    flow2 = create_flow_from_yaml('flows/pipeline2.yaml')
    flow2(html_path='/workspaces/rag-data-pipeline/data/1.html', markdown_output_path='/workspaces/rag-data-pipeline/data/1.md')

    # Example: Running Pipeline 3
    flow3 = create_flow_from_yaml('flows/pipeline3.yaml')
    flow3(pdf_path='/workspaces/rag-data-pipeline/data/1.pdf', api_response_output_path='/workspaces/rag-data-pipeline/data/3_1.json')

if __name__ == "__main__":
    main()
