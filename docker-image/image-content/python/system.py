import os

def get_gradify_base_dir():
  return os.getenv("GRADIFY_DIR")

def get_project_config_filename():
  return os.getenv("PRJ_CONFIG_FILENAME")
