import os
from wol.credentials import ADMINS

LIST_OF_ADMINS = [] + ADMINS

UNAUTHORIZED_ERROR_MESSAGE = "Private Bot: You are not allowed to use this bot!"

# DB_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# DB_PATH = f"sqlite:///{DB_ROOT}/db.db"
DB_ROOT = "sqlite:///../"
DB_PATH = f"{DB_ROOT}db.db"
