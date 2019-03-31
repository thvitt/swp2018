import os
import logging
import logging.config
import yaml

def setup_logging(
        default_path='logging_config.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'):
    """Sets up the logging configuration.
    
        Args:
            default_path (string) -- Path to the logging config yaml-file.
            default_level (int) -- Level of the logging message.
            env_key (string) -- Name of the environment variable.
            
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration')
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
