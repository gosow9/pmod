import yaml
import os

class ConfigHandler:
    def __init__(self, config_path=None):
        """
        Initialize the ConfigHandler with the path to the YAML configuration file.
        Args:
        - config_path (str): Path to the YAML configuration file
        """
        if config_path is None:
            # Get the directory of this script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, 'config.yml')
        
        self.config_path = config_path
        self.config_data = self._load_config()


    def _load_config(self):
        """
        Load the configuration from the YAML file.
        Returns:
        - dict: Configuration data
        """
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key_path, default=None):
        """
        Get the value for a given key or key path from the configuration.
        Args:
        - key_path (str): Dot-separated path to the key (e.g. 'parent.child.key')
        - default (any, optional): Default value if key doesn't exist
        Returns:
        - any: Value associated with the key or key path
        """
        keys = key_path.split('.')
        data = self.config_data
        for key in keys:
            data = data.get(key)
            if data is None:
                return default
        return data
    
    
    def get_top_level_keys(self):
        """
        Get all the top-level keys from the configuration.
        Returns:
        - list: List of top-level keys
        """
        return list(self.config_data.keys())
    

    def set(self, key_path, value):
        """
        Set a value for a given key path in the configuration.
        Args:
        - key_path (str): Dot-separated path to the key (e.g. 'parent.child.key')
        - value (any): Value to set
        """
        keys = key_path.split('.')
        data = self.config_data
        for key in keys[:-1]:  # all but last
            data = data.setdefault(key, {})
        data[keys[-1]] = value

    def save(self):
        """
        Save the current configuration back to the YAML file.
        """
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config_data, file)
    
    
            
        

if __name__ == "__main__":
    handler = ConfigHandler('config.yml')
    print(handler.get('brewer.path')) # DeviceA
    handler.set('brewer.new', 'Device')
    handler.save()

    
