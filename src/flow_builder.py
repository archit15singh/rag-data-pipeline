# src/flow_builder.py
import yaml
from prefect import Flow, Parameter
from tasks import read_pdf, chunk_text, write_json, read_html, convert_html_to_markdown, write_file, call_api

def create_flow_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    with Flow(config['flow_name']) as flow:
        parameters = {}
        tasks = {}
        for param in config.get('parameters', []):
            parameters[param['name']] = Parameter(param['name'], default=param.get('default'))

        for task_config in config['tasks']:
            task_name = task_config['name']
            task_params = {k: parameters.get(v, v) for k, v in task_config['params'].items()}
            
            if task_name == 'read_pdf':
                tasks[task_name] = read_pdf(**task_params)
            elif task_name == 'chunk_text':
                tasks[task_name] = chunk_text(tasks[task_params['input']], chunk_size=task_params.get('chunk_size', 100))
            elif task_name == 'write_json':
                tasks[task_name] = write_json(tasks[task_params['input']], output_path=task_params['output_path'])
            elif task_name == 'read_html':
                tasks[task_name] = read_html(**task_params)
            elif task_name == 'convert_html_to_markdown':
                tasks[task_name] = convert_html_to_markdown(tasks[task_params['input']])
            elif task_name == 'write_file':
                tasks[task_name] = write_file(tasks[task_params['input']], output_path=task_params['output_path'])
            elif task_name == 'call_api':
                tasks[task_name] = call_api(file_name=task_params['file_name'])
            # Add more tasks as needed...

    return flow
