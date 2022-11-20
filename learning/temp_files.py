import os
import tempfile


def create_temp_file():
    with tempfile.NamedTemporaryFile() as tmp:
        print(f"File '{tmp.name}' is created")
        print(f"Exists '{os.path.exists(tmp.name)=}'")
        print(f"Is file '{os.path.isfile(tmp.name)=}'")
        print(f"abspath '{os.path.abspath(tmp.name)=}'")
        print(f"")


def create_temp_file_with_props():
    with tempfile.NamedTemporaryFile(dir=os.path.curdir) as tmp:
        tmp.name = "a_random_file.with_extension"
        print(f"File '{tmp.name}' is created")
        print(f"Exists '{os.path.exists(tmp.name)=}'")
        print(f"Is file '{os.path.isfile(tmp.name)=}'")
        print(f"abspath '{os.path.abspath(tmp.name)=}'")
        print(f"")


def create_temp_file_in_temp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        print(f"Dir '{tmp_dir}' is created")

        tmp_file = tempfile.NamedTemporaryFile(dir=tmp_dir)
        print(f"File '{tmp_file.name}' is created")
        print(f"Exists '{os.path.exists(tmp_file.name)=}'")
        print(f"Is file '{os.path.isfile(tmp_file.name)=}'")
        print(f"abspath '{os.path.abspath(tmp_file.name)=}'")
        print(f"")


if __name__ == '__main__':
    create_temp_file()
    create_temp_file_with_props()
    create_temp_file_in_temp_dir()
