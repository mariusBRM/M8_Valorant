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

