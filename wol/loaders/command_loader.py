import pluggy
from .loader import PluginLoader

COMMAND_PROJECT_NAME = "commands"

commands_hookspec = pluggy.HookspecMarker(COMMAND_PROJECT_NAME)
commands_foo = pluggy.HookimplMarker(COMMAND_PROJECT_NAME)


class CommandLoader(PluginLoader):
    DEFAULT_PLUGINS_PATH = 'wol/commands'
    DEFAULT_PLUGINS_PACKAGE = 'wol.commands'

    def __init__(self):
        super(CommandLoader, self).__init__(COMMAND_PROJECT_NAME,
                                            CommandHookSpec,
                                            plugin_path=self.DEFAULT_PLUGINS_PATH,
                                            plugin_package=self.DEFAULT_PLUGINS_PACKAGE)


class CommandHookSpec:
    """
    A hook specification namespace for the commands.
    """

    @commands_hookspec
    def init(self, **kwargs):
        return

    @commands_hookspec
    def register_handlers(self, dispatcher, **kwargs):
        """
        This hook will register all handlers for the specific command

        :param dispatcher: the Telegram Bot dispatcher
        """
        return None

    @commands_hookspec
    def get_foo_to_push(self, **kwrgs) -> list:
        """
        This hook will return a list of functions to be pushed as part of the main class
        """
        return []
