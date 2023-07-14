import os
import pickle


def dump_data(new_data, dump_file, stage):
    # Load existing data from the old dump file
    existing_data = []

    if stage == 0:
        print("create new dump file:", dump_file)

    if stage > 0:
        try:
            with open(dump_file, 'rb') as file:
                existing_data = pickle.load(file)
        except FileNotFoundError:
            print("create new dump file:", dump_file)

    combined_data = existing_data + new_data
    # Dump the combined data into the file
    with open(dump_file, 'wb') as file:
        pickle.dump(combined_data, file)


def read_dump(stage):
    # Load the dump data and fails
    data = []
    fails = []
    try:
        with open(f'data_{stage}.pickle', 'rb') as file:
            data = pickle.load(file)
    except FileNotFoundError:
        print(f"no dump data found 'data_{stage}.pickle'")

    try:
        with open(f'fails_{stage}.pickle', 'rb') as file:
            fails = pickle.load(file)
    except FileNotFoundError:
        print(f"no dump data found 'fails_{stage}.pickle'")

    return data, fails


def dump_stage(partial, fails, stage=0):
    dump_data(partial, f"data_{stage}.pickle", stage)
    if stage > 0:
        dump_data(fails, f"fails_{stage}.pickle", stage)


def clear_damp():
    directory = os.getcwd()  # Get the current working directory

    for filename in os.listdir(directory):
        if filename.endswith(".pickle"):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Deleted file: {filename}")
