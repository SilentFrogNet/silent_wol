import re

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters
)

from wol.utils import utils
from wol.utils.decorators import (
    send_typing_action,
    restricted
)

from wol.loaders.command_loader import commands_foo


class RegisterCommand(object):

    def __init__(self):
        self.re_mac = re.compile(r'^([ ]*([0-9a-fA-F]{2}[:]{0,1}){5}[0-9a-fA-F]{2}[ ]*)$')
        self.register_tmps = {}

    @commands_foo
    def init(self):
        self.register_tmps = {}

    @commands_foo
    def register_handlers(self, dispatcher):
        register_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('register', self.register)],

            states={
                utils.RegisterDeviceStates.NAME: [MessageHandler(Filters.text, self._register_name)],
                utils.RegisterDeviceStates.MAC: [MessageHandler(Filters.text, self._register_mac)]
            },

            fallbacks=[CommandHandler('cancel', self._register_cancel)]
        )
        dispatcher.add_handler(register_conv_handler)

    @commands_foo
    def get_foo_to_push(self):
        return [
            self.register,
            self._register_name,
            self._register_mac,
            self._register_cancel
        ]

    @staticmethod
    @send_typing_action
    @restricted
    def register(update, context):
        """
        This will reply to the `/register` command
        """
        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text="Welcome to the register wizard.\n"
                 "Send /cancel to stop the registration process.\n\n"
                 "Let's start with the device name"
        )

        return utils.RegisterDeviceStates.NAME

    @send_typing_action
    @restricted
    def _register_name(self, update, context):
        """
        Handles the registration process for the name
        """
        tmp_dev_name = update.message.text
        self._register_tmp_value(utils.get_chat_id(update, context), 'name', tmp_dev_name)
        self.logger.info(f"Registering device name \"{tmp_dev_name}\"")

        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text="Now give me the MAC address of the device"
        )

        return utils.RegisterDeviceStates.MAC

    @send_typing_action
    @restricted
    def _register_mac(self, update, context):
        """
        Handles the registration process for the mac
        """
        tmp_dev_mac = update.message.text
        chat_id = utils.get_chat_id(update, context)
        self._register_tmp_value(chat_id, 'mac', tmp_dev_mac)
        self.logger.info(f"Registering device mac \"{tmp_dev_mac}\"")

        status_code, err_msg = self._register_device(chat_id)
        if status_code == utils.StatusCodes.OK:
            response_message = f"Cool! the device ({self.register_tmps.get(chat_id, {}).get('name', '')} - {self.register_tmps.get(chat_id, {}).get('mac', '')}) is successfully registered!"
            self._register_reset_tmps(chat_id)
        elif status_code == utils.StatusCodes.MAC_ADDRESS_ALREADY_EXISTS:
            response_message = f"The MAC address for {self.register_tmps.get(chat_id, {}).get('name', '')} already exists! If you want to update that device use the /edit command. Abort!"
            self._register_reset_tmps(chat_id)
        else:
            response_message = f"A generic error occurred: {err_msg}. Abort!"
            self._register_reset_tmps(chat_id)

        context.bot.send_message(
            chat_id=chat_id,
            text=response_message
        )

        return ConversationHandler.END

    @send_typing_action
    @restricted
    def _register_cancel(self, update, context):
        """
        Handles the cancel of the registration process
        """
        self._register_reset_tmps(utils.get_chat_id(update, context))

        context.bot.send_message(
            chat_id=utils.get_chat_id(update, context),
            text=f"Ok, process cancelled. Bye!"
        )

        return ConversationHandler.END

    @send_typing_action
    @restricted
    def _register_device(self, chat_id):
        tmps = self.register_tmps.get(chat_id, None)
        if not tmps:
            self.logger.critical(f"Missing chat_id ({chat_id}) in self.register_tmps")
            return utils.StatusCodes.PROCESS_ERROR, "Missing chat_id in self.register_tmps"

        name = tmps.get('name', None)
        if not name:
            self.logger.critical(f"Missing name for chat_id ({chat_id})")
            return utils.StatusCodes.MISSING_NAME, "Missing name for chat_id"

        mac = tmps.get('mac', None)
        if not mac:
            self.logger.critical(f"Missing MAC address for chat_id ({chat_id})")
            return utils.StatusCodes.MISSING_MAC, "Missing MAC address for chat_id"

        if mac in self.devices:
            self.logger.warning(f"MAC address ({mac}) already registered!")
            return utils.StatusCodes.MAC_ADDRESS_ALREADY_EXISTS, "MAC address already registered!"

        if not self.re_mac.match(mac):
            self.logger.warning(f"Invalid MAC address ({mac})!")
            return utils.StatusCodes.MAC_ADDRESS_INVALID, "Invalid MAC address!"

        with utils.DBWrapper() as db:
            db.insert_device(name, mac)
        self.devices[name] = mac
        return utils.StatusCodes.OK, None

    def _register_tmp_value(self, chat_id, key, value):
        """
        Stores a temporary value during the registration process

        :param chat_id: the chat id
        :param key: the key-reference for the value
        :param value: the value to store
        """
        if chat_id not in self.register_tmps:
            self.register_tmps[chat_id] = {}
        self.register_tmps[chat_id][key] = value

    def _register_reset_tmps(self, chat_id):
        """
        Removes all the temporary values for the specified chat id

        :param chat_id: the chat id
        """
        if chat_id in self.register_tmps:
            del self.register_tmps[chat_id]
