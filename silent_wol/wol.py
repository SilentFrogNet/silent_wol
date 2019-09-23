import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    Filters
)

from silent_wol.credentials import (
    bot_token,
    bot_user_name
)
from silent_wol.utils import utils
from silent_wol.register_mixin import WoLRegisterMixin
from silent_wol.utils.decorators import (
    restricted,
    send_typing_action
)
from silent_wol import settings


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class SilentWolBot(WoLRegisterMixin):
    """ The Silent WOL Bot """

    WOL_PREFIX = "wol_"
    SOL_PREFIX = "sol_"
    EDIT_PREFIX = "edit_"
    DELETE_PREFIX = "del_"

    def __init__(self, name=bot_user_name):
        self.name = name
        self.updater = Updater(token=bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.logger = logging.getLogger(__name__)

        self.conn = utils.db.connect()

        self.devices = {
            'Ilario\'s PC': '11:22:33:44:aa:bb',
            'Raspberry Pi': '1a:2f:ff:e4:a4:2b',
        }

        self.init_register()

        self.register_handlers()

    def run_bot(self):
        self.logger.info(f"Starting {self.name}")
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def stop_bot(self):
        self.logger.info(f"Stopping {self.name}")
        self.conn.close()
        self.updater.stop()

    def register_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('help', self.help))
        self.dispatcher.add_handler(CommandHandler('edit', self.edit))
        self.dispatcher.add_handler(CommandHandler('delete', self.delete))
        self.dispatcher.add_handler(CommandHandler('wakeup', self.wakeup))
        self.dispatcher.add_handler(CommandHandler('sleep', self.sleep))
        self.dispatcher.add_handler(CommandHandler('list', self.list))

        # Register mixin's handlers
        self.register_handler_register()

        # Callback query handlers
        self.dispatcher.add_handler(CallbackQueryHandler(self._wol_handler, pattern=f'{self.WOL_PREFIX}.*?'))
        self.dispatcher.add_handler(CallbackQueryHandler(self._sol_handler, pattern=f'{self.SOL_PREFIX}.*?'))
        self.dispatcher.add_handler(CallbackQueryHandler(self._edit_handler, pattern=f'{self.EDIT_PREFIX}.*?'))
        self.dispatcher.add_handler(CallbackQueryHandler(self._delete_handler, pattern=f'{self.DELETE_PREFIX}.*?'))

        # log all errors
        self.dispatcher.add_error_handler(self.error)

        # Manage all unknown commands
        self.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

    def error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

    @send_typing_action
    def start(self, update, context):
        """
        This will reply to the `/start` command
        """
        chat_id = utils.get_chat_id(update, context)
        self.logger.debug(f"Talking to: {chat_id}")
        print(f"Talking to: {chat_id}")

        if chat_id not in settings.LIST_OF_ADMINS:
            msg = settings.UNAUTHORIZED_ERROR_MESSAGE
        else:
            msg = f"Hello! I'm {self.name}. With me you can \"Wake on LAN\" your device! Use /help to have more info!"

        context.bot.send_message(
            chat_id=chat_id,
            text=msg
        )

    @send_typing_action
    @restricted
    def help(self, update, context):
        """
        This will reply to the `/help` command
        """
        help_text = """
I can help you register and manage WoL enabled devices.

You can control me by sending these commands:

/register - registers a new device
/edit - edits the device
/delete - removes the device
/wakeup - wakes up the device
/sleep - puts the device back to sleep
"""
        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text=help_text
        )

    @send_typing_action
    @restricted
    def edit(self, update, context):
        """
        This will reply to the `/edit` command
        """
        reply_markup = self._build_devices_menu(self.EDIT_PREFIX)
        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text="Choose the device to edit:",
            reply_markup=reply_markup
        )

    @send_typing_action
    @restricted
    def delete(self, update, context):
        """
        This will reply to the `/delete` command
        """
        reply_markup = self._build_devices_menu(self.DELETE_PREFIX)
        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text="Choose the device to delete:",
            reply_markup=reply_markup
        )

    @send_typing_action
    @restricted
    def wakeup(self, update, context):
        """
        This will reply to the `/wakeup` command
        """
        reply_markup = self._build_devices_menu(self.WOL_PREFIX)
        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text="Choose the device to wake up:",
            reply_markup=reply_markup
        )

    @send_typing_action
    @restricted
    def sleep(self, update, context):
        """
        This will reply to the `/sleep` command
        """
        reply_markup = self._build_devices_menu(self.SOL_PREFIX)
        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text="Choose the device to wake up:",
            reply_markup=reply_markup
        )

    @send_typing_action
    @restricted
    def list(self, update, context):
        """
        This will reply to the `/list` command
        """
        list_text = ", ".join([d for d in self.devices.keys()])
        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text=list_text
        )

    @send_typing_action
    @restricted
    def unknown(self, update, context):
        """
        This will reply to all unknown commands
        """
        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text="Sorry, I didn't understand that command. Use /help to have more info!"
        )

    def _build_devices_menu(self, action, cancel_button=True):
        button_list = [InlineKeyboardButton(dev, callback_data=f"{action}{dev}") for dev in self.devices.keys()]
        if cancel_button:
            button_list.append(InlineKeyboardButton("Cancel", callback_data=f"{action}cancel"))
        return InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=4))

    def _wol_handler(self, update, context):
        """
        This will handle the callback of the wol (/wakeup) action
        """
        dev = update.callback_query.data.lstrip(self.WOL_PREFIX)
        chat_id = utils.get_chat_id(update, context)

        if dev == "cancel":
            context.bot.send_message(
                chat_id=chat_id,
                text="Operation cancelled!"
            )
            return

        mac = self.devices.get(dev, None)

        context.bot.send_message(
            chat_id=chat_id,
            text=f"WoL {mac}!"
        )

    def _sol_handler(self, update, context):
        """
        This will handle the callback of the sol (/sleep) action
        """
        dev = update.callback_query.data.lstrip(self.SOL_PREFIX)
        chat_id = utils.get_chat_id(update, context)

        if dev == "cancel":
            context.bot.send_message(
                chat_id=chat_id,
                text="Operation cancelled!"
            )
            return

        mac = self.devices.get(dev, None)

        context.bot.send_message(
            chat_id=chat_id,
            text=f"SoL {mac}!"
        )

    def _edit_handler(self, update, context):
        """
        This will handle the callback of the edit action
        """
        dev = update.callback_query.data.lstrip(self.EDIT_PREFIX)
        chat_id = utils.get_chat_id(update, context)

        if dev == "cancel":
            context.bot.send_message(
                chat_id=chat_id,
                text="Operation cancelled!"
            )
            return

        context.bot.send_message(
            chat_id=chat_id,
            text=f"Editing {dev}!"
        )

    def _delete_handler(self, update, context):
        """
        This will handle the callback of the delete action
        """
        dev = update.callback_query.data.lstrip(self.DELETE_PREFIX)
        chat_id = utils.get_chat_id(update, context)

        if dev == "cancel":
            context.bot.send_message(
                chat_id=chat_id,
                text="Operation cancelled!"
            )
            return

        self.db.delete_device(name, mac)

        context.bot.send_message(
            chat_id=chat_id,
            text=f"Device {dev} deleted!"
        )
