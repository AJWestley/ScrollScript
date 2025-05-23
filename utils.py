from keywords import KEYWORDS_LIST, INTEGER, FLOAT

def is_keyword(name):
    """
    Checks if a name is a language constant.

    Args:
        name (str): The value to check.

    Returns:
        bool: True if it is a constant, False otherwise.
    """
    return name in KEYWORDS_LIST

def is_number(name):
    """
    Checks if a variable is a number.

    Args:
        name: The variable to check.

    Returns:
        bool: True if it is a float or int, False otherwise.
    """
    return name.type_name in [INTEGER, FLOAT]

def load_file(file_path):
    """
    Loads the content of a text file into a string.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The content of the file as a string, or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
