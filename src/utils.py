import shutil


GREEN = '\033[92m'
HEADER = '\033[95m'
RED = '\033[91m'
YELLOW = '\033[93m'
WHITE = '\033[0m'


def remove_directory(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        print(f"Directory '{path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while removing directory '{path}': {str(e)}")
