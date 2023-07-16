import os
import pickle


def dump(data, dump_file):
    with open(dump_file, 'wb') as file:
        pickle.dump(data, file)


def read_dump(dump_file):
    try:
        with open(dump_file, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"no dump data found '{dump_file}'")

    return None


def clear_dump():
    directory = os.getcwd()  # Get the current working directory

    for filename in os.listdir(directory):
        if filename.endswith(".pickle"):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Deleted file: {filename}")
