import contextlib
import json


@contextlib.contextmanager
def json_open(filepath: str, mode: str):
    """
    Reads a JSON file from file path, with supplied mode, and returns JSON accessor object.
    Usage:

    .. code-block:: python

    with json_read("file.json", "r") as json_data:
        print(json_data)

        # Other operations here...

    
    :param filepath: File path
    :param mode: Mode to open file ("r", "rw", etc.)
    :return: 
    """
    file = open(filepath, mode)
    try:
        yield json.load(file)
    finally:
        file.close()
