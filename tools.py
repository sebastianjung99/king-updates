import coloredlogs, logging
import time
import os
import json


# configurate logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler("log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(coloredlogs.ColoredFormatter(log_format))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


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