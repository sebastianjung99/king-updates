import coloredlogs, logging
import time
import os
import json


# configurate logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

LOG_FORMAT = "%(asctime)s - %(levelname)-8s - %(name)-20s - %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler("log.log")
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.DEBUG)
STREAM_HANDLER.setFormatter(coloredlogs.ColoredFormatter(LOG_FORMAT))

LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)


def get_time_f():
    """
    Gets current time.
    
    Returns:
    ------------
    :class:`str`
       Time formatted to `mm/dd/yyyy HH:MM:SS`
    """
    
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)
    return time_string


def append_txt(file_name: str, append_str: str, relative_path: str = "", timestamp: bool = True):
    """
    Appends given string to txt-file.

    Parameters:
    ------------
    file_name: :class:`str`
        Name of the file to append to with file extension.
    append_str :class:`str`
        String to append at the bottom of the file.
    relative_path: Optional [:class:`str`]
        Relative path of the file.
            Example: Working directory is in C:\work and file in C:\work\\file. `relative_path` = \"\\file\"
    timestamp: Optional [:class:`bool`]
        Wether to put date and time in front of the string. 
        Defaults to `True`.

    Raises:
    ------------
    FileNotFoundError
        Raised when a file or directory is requested but doesn’t exist. Corresponds to errno ENOENT.

    Returns:
    ------------
    :class:`bool`
    Wether operation was succesfull or not.
    """
    
    dir = os.path.dirname(os.path.realpath(__file__)) + relative_path
    try:        
        with open(f'{dir}\{file_name}', 'a') as f:
            if timestamp:
                f.write(f'\n{get_time_f()}\t{append_str}')
            elif not timestamp:
                f.write(f'\n{append_str}')
                
        return True

    except Exception as e:
        logging.exception(e)
        return False
    

def get_json(file_name: str, relative_path: str = ""):
    """
    Loads a json file and returns it as a dict.
    
    Parameters:
    ------------
    file_name: :class:`str`
        Name of the file to load json from, with file extension.
    relative_path: Optional [:class:`str`]
        Relative path of the file.
            Example: Working directory is in C:\work and file in C:\work\\file. `relative_path` = \"\\file\"

    Raises:
    ------------
    FileNotFoundError
        Raised when a file or directory is requested but doesn’t exist. Corresponds to errno ENOENT.

    Returns:
    ------------
    :class:`dict`
        Parsed json file as dictionary if operation was succesfull.
    `False`
    If operation failed.
    """
    
    dir = os.path.dirname(os.path.realpath(__file__)) + relative_path
    try:
        with open(f'{dir}\{file_name}', 'r') as f:
            return json.load(f)
        
    except Exception as e:
        logging.exception(e)
        return False