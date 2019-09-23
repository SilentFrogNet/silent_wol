import os
from silent_wol.credentials import admins

LIST_OF_ADMINS = [] + admins

UNAUTHORIZED_ERROR_MESSAGE = "Private Bot: You are not allowed to use this bot!"

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3'))
