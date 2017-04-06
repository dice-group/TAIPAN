import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBJECT_COLUMN_LIST = os.path.join(CURRENT_DIR, "..", "data", "subject_column_list.csv")
CLASSES_LIST = os.path.join(CURRENT_DIR, "..", "data", "classes_list.csv")
TABLES_DIR = os.path.join(CURRENT_DIR, "..", "data", "tables")
PROPERTIES_DIR = os.path.join(CURRENT_DIR, "..", "data", "properties")
ENTITIES_DIR = os.path.join(CURRENT_DIR, "..", "data", "entities")
DEFAULT_CACHE_DIR = os.path.join(CURRENT_DIR, "..", "cache")
