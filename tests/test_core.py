import pytest


from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters
)

from silent_wol.core.wol import SilentWolBot

# --- [DATA] --- #
# sho_items_data = [
#     {
#         'name': 'demo',
#         'description': 'Demo server',
#         'host': '192.168.1.2',
#         'shell_type': ShoTypes.SSH
#     },
#     {
#         'name': 'zsh',
#         'description': 'Oh My Zsh!',
#         'shell_type': ShoTypes.LOCAL
#     }
# ]
#
# sho_items_invalid_data = [
#     {
#         'name': 'invalid',
#         'description': 'invalid match type-host',
#         'shell_type': ShoTypes.LOCAL,
#         'host': '192.168.1.2'
#     }
# ]
# --- [/DATA] --- #


# --- [FIXTURES] --- #
@pytest.fixture
def bot():
    """ Creates Silent WoL Bot fixture to use in other tests"""
    return SilentWolBot()

# @pytest.fixture(params=sho_items_data)
# def sho_item_dict(request, sho):
#     """ Creates valid ShoItem from dict fixture to use in other tests"""
#     yield sho.add_item(ShoItem(**request.param))
#
#
# @pytest.fixture(params=sho_items_data)
# def sho_item(request, sho):
#     """ Creates valid ShoItem fixture to use in other tests"""
#     yield sho.add(
#         item_name=request.param.get('name', None),
#         item_type=request.param.get('shell_type', None),
#         item_description=request.param.get('description', None),
#         item_host=request.param.get('host', None)
#     )
# --- [/FIXTURES] --- #


# --- [SUPPORT FUNCTIONS] --- #
# def add_valid_shells(sho: Sho) -> None:
#     for s in sho_items_data:
#         sho.add_item(ShoItem(**s))


def compare_lists(list1: list, list2: list) -> None:
    """ Compares two lists and checks if they are equal """
    found = True
    for el in list1:
        if found and el not in list2:
            found = False
            break
    return found
# --- [/SUPPORT FUNCTIONS] --- #


# --- [TESTS] --- #
def test_creation(bot:SilentWolBot) -> None:
    assert isinstance(bot, SilentWolBot)
    assert isinstance(bot.name, str)
    assert bot.name != ''
    assert isinstance(bot.updater, Updater)
#
#
#
# def test_create_sho() -> None:
#     """ Tests the creation of a Sho instance """
#     sho = Sho()
#     assert isinstance(sho, Sho), "No valid instance of Sho"
#
#
# def test_get_list_of_shells_empty(sho: Sho) -> None:
#     """ Tests the get of an empty list """
#     shells = sho.list()
#     assert isinstance(shells, list), "should be a list"
#     assert shells == [], "Should be an empty list"
#
#
# def test_create_sho_item_dict(sho_item_dict: ShoItem) -> None:
#     """ Tests the creation of a ShoItem instance from dict """
#     assert isinstance(sho_item_dict, ShoItem)
#
#
# def test_create_sho_item(sho_item: ShoItem) -> None:
#     """ Tests the creation of a ShoItem instance """
#     assert isinstance(sho_item, ShoItem)
#
#
# def test_create_invalid_sho_item() -> None:
#     """ Tests the creation of an invalid ShoItem that raises exception """
#     for i in sho_items_invalid_data:
#         with pytest.raises(InconsistentParametersError) as e:
#             ShoItem(**i)
#         assert str(e.value) == "Host is not supported with a non-remote shell_type."
#
#
# def test_create_duplicated_sho_item(sho: Sho) -> None:
#     """ Tests the creation of an already existing ShoItem that raises exception """
#     sho.add_item(ShoItem(**sho_items_data[0]))
#     with pytest.raises(AlreadyExistingShellError) as e:
#         item = ShoItem(**sho_items_data[0])
#         sho.add_item(item)
#     assert str(e.value) == "Shell already exists."
#
#
# def test_get_list_of_shells(sho: Sho) -> None:
#     """ Tests the get of a list """
#     add_valid_shells(sho)
#     shells = sho.list()
#     assert isinstance(shells, list), "Should be a list"
#     assert len(shells) == 2, "Should have only 2 elements"
#
#
# def test_get_list_of_ssh_shells(sho: Sho) -> None:
#     """ Tests the get of a list filtered by ssh """
#     add_valid_shells(sho)
#     shells = sho.list(shell_type=ShoTypes.SSH)
#     assert isinstance(shells, list), "Should be a list"
#     assert len(shells) == 1, "Should have only one element"
#     assert shells[0].name == sho_items_data[0]['name']
#     assert shells[0].type == sho_items_data[0]['shell_type']
#     assert shells[0].description == sho_items_data[0]['description']
#     assert shells[0].host == sho_items_data[0]['host']
#
#
# def test_get_list_of_shells_string(sho: Sho) -> None:
#     add_valid_shells(sho)
#     shells = sho.strlist()
#     assert isinstance(shells, list)
#     assert len(shells) == 2, "Should have only 2 elements"
#
#     names = [s['name'] for s in sho_items_data]
#     assert compare_lists(shells, names)
#
#
# def test_get_list_of_shells_string_verbose(sho: Sho) -> None:
#     add_valid_shells(sho)
#     sho.verbose = True
#     shells = sho.strlist()
#     assert isinstance(shells, list)
#     assert len(shells) == 2, "Should have only 2 elements"
#
#     names = ['ssh\t@ demo(192.168.1.2)', 'local\t@ zsh']
#     assert compare_lists(shells, names)
#
#
# def test_get_sho_item(sho: Sho, sho_item: ShoItem) -> None:
#     """ Tests the get of a single ShoItem instance """
#     retrieved_item = sho.get(sho_item.name)
#
#     assert retrieved_item.name == sho_item.name
#     assert retrieved_item.type == sho_item.type
#     assert retrieved_item.description == sho_item.description
#     assert retrieved_item.host == sho_item.host
#
#
# def test_get_sho_item_not_found(sho: Sho) -> None:
#     """ Tests the get of a single ShoItem instance """
#     with pytest.raises(ShellNotFoundError) as e:
#         sho.get("NOT FOUND ITEM")
#     assert str(e.value) == "Shell not found."
# --- [/TESTS] --- #
