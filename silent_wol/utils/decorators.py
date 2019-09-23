from functools import wraps
from telegram import ChatAction

from silent_wol.utils import utils
from silent_wol import settings


def get_user_id(update, context):
    try:
        return context.effective_user.id
    except Exception:
        return update.effective_user.id


def get_bot(update, context):
    try:
        return update.updater.bot
    except Exception:
        return context.bot


def get_logger(update, context):
    try:
        return update.logger
    except Exception:
        return context.bot.logger


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = get_user_id(update, context)
        if user_id not in settings.LIST_OF_ADMINS:
            get_logger(update, context).warning(f"Unauthorized access denied for {user_id}.")
            get_bot(update, context).send_message(
                chat_id=utils.get_chat_id(update, context),
                text=settings.UNAUTHORIZED_ERROR_MESSAGE
            )
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            get_bot(update, context).send_chat_action(
                chat_id=utils.get_chat_id(update, context),
                action=action
            )
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
