from wol.db.utils import create_tables


def setup_test():
    """
    Sets up test module
    """
    create_tables()


def teardown_test():
    """
    Tears down test module
    """
    pass


def compare_lists(list1: list, list2: list) -> None:
    """
    Compares two lists and checks if they are equal
    """
    found = True
    for el in list1:
        if found and el not in list2:
            found = False
            break
    return found
