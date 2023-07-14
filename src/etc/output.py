import os

from .utils import GREEN, WHITE


def output(items, fails, stage=0):
    file = f"stage_{stage}.yml"
    if stage == 2:
        file = "output.yml"

    # delete old stage output file if exist
    if os.path.exists(file):
        os.remove(file)
        print(f"stage {stage} outdated output file deleted, creating a new one {file}")

    print(f"writing stage output to YAML file {file}", end=" ")

    # write output in YAML file
    with open(file, "w") as f:
        if items:
            f.write("items:\n")
            for item in items:
                f.write(f"  - title: \"{item.get('title')}\"\n")
                f.write(f"    url: {item.get('url')}\n")
        if fails and stage > 0:
            f.write("fails:\n")
            for fail in fails:
                f.write(f"  - title: \"{fail.get('title')}\"\n")
                f.write(f"    url: {fail.get('url')}\n")
                f.write(f"    error: {fail.get('error')}\n")

    print(f"{GREEN}OK{WHITE}")
