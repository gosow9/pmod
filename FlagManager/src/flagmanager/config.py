import yaml

# Load the yaml file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

print(config)
