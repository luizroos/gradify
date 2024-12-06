import os

def get_gradify_base_dir():
  return os.getenv("GRADIFY_DIR")

def get_gradify_tools_dir():
  return os.getenv("GRADIFY_TOOLS_DIR")

def get_project_config_filename():
  return os.getenv("PRJ_CONFIG_FILENAME")

def is_debug_mode():
  return os.getenv("GRATIFY_DEBUG")
