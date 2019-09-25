import os

bot_token = os.getenv('BOT_TOKEN', '')
bot_user_name = "Silent WoL Bot"

admins = [s.strip() for s in os.getenv('ADMINS', '').split(';')]
