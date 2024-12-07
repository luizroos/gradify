import os
from dataclasses import dataclass

def get_gradify_tools_dir():
  return os.getenv("GRADIFY_TOOLS_DIR")

def is_debug_mode():
  return os.getenv("GRATIFY_DEBUG")
