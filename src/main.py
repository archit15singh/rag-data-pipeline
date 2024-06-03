# src/main.py
from flow_builder import create_flow_from_yaml

# Example: Running Pipeline 1
flow = create_flow_from_yaml('../flows/pipeline1.yaml')
flow.run()

# Example: Running Pipeline 2
flow = create_flow_from_yaml('../flows/pipeline2.yaml')
flow.run()

# Example: Running Pipeline 3
flow = create_flow_from_yaml('../flows/pipeline3.yaml')
flow.run()
