import yaml
from pathlib import Path

class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self):
        # Load the YAML configuration file
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def get_data_path(self, data_type: str) -> Path:
        # Retrieve a specific data path from the config
        try:
            return Path(self.config_data['data_paths'][data_type])
        except KeyError:
            raise ValueError(f"No data path found for: {data_type}")
        
    def get_api_key_from_file(self, file_path):
        """
        Reads an API key from a text file and returns it.
        
        :param file_path: Path to the file containing the API key.
        :return: API key as a string or None if not found.
        """
        try:
            with open(file_path, 'r') as file:
                api_key = file.read().strip()  # Read and remove any extra whitespace/newlines
                return api_key
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

