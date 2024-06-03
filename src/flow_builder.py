import yaml
from prefect import flow, get_run_logger
from tasks import read_pdf, chunk_text, write_json, read_html, convert_html_to_markdown, write_file, call_api

def create_flow_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    @flow(name=config['flow_name'])
    def dynamic_flow(**kwargs):
        logger = get_run_logger()
        tasks = {
            'read_pdf': read_pdf,
            'chunk_text': chunk_text,
            'write_json': write_json,
            'read_html': read_html,
            'convert_html_to_markdown': convert_html_to_markdown,
            'write_file': write_file,
            'call_api': call_api,
        }
        results = {}
        for task_config in config['tasks']:
            task_name = task_config['name']
            task_params = {}
            dependencies = []
            
            for param_key, param_value in task_config['params'].items():
                if param_value in results:
                    task_params[param_key] = results[param_value]
                else:
                    task_params[param_key] = kwargs.get(param_value, param_value)

            if 'depends_on' in task_config:
                depends_on = task_config['depends_on']
                if isinstance(depends_on, list):
                    dependencies = [results[dep] for dep in depends_on]
                else:
                    dependencies = [results[depends_on]]

            logger.info(f"Running task: {task_name} with params: {task_params} and dependencies: {dependencies}")

            if task_config.get('parallel', False):
                try:
                    results[task_name] = tasks[task_name].submit(*dependencies, **task_params)
                except Exception as e:
                    logger.error(f"Task {task_name} failed")
                    raise
            else:
                try:
                    results[task_name] = tasks[task_name](*dependencies, **task_params)
                except Exception as e:
                    logger.error(f"Task {task_name} failed")
                    raise

        return results

    return dynamic_flow
