import yaml

def read_config(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error while parsing YAML file: {e}")
        return None

# Example usage:
yaml_file_path = "config.yml"
CONFIG = read_config(yaml_file_path)

