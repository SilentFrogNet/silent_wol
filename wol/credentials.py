"""
    Stores all credentials for the bot
"""

import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
BOT_USER_NAME = "Silent WoL Bot"

ADMINS = [int(s.strip()) for s in os.getenv('ADMINS', '').split(';')]
