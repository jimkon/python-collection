import os
import pathlib
from collections import Counter, OrderedDict
import zlib

from tqdm import tqdm


class FileSet:
    def __init__(self, files):
        self._all_files = files

    @classmethod
    def from_path(self, path):
        files = [str(file) for file in sorted(pathlib.Path(path).rglob('*'))]
        return FileSet(files)

    @property
    def files(self):
        return self._all_files

    def find_dirs(self):
        return {str(pathlib.Path(file).parent) for file in self.files}

    @property
    def pathlib_files(self):
        return [pathlib.Path(file) for file in self.files]

    def filter_extensions(self, exts):
        exts = [exts] if isinstance(exts, str) else exts

        res_files = []
        for file in self.files:
            ext = pathlib.Path(file).suffix
            if ext in exts:
                res_files.append(file)
        return FileSet(res_files) if len(res_files)>0 else None

    def exclude_string_in_path(self, dirs):
        dirs = [dirs] if isinstance(dirs, str) else dirs

        res_files = self.files.copy()
        for file in self.files:
            for _dir in dirs:
                if _dir in file:
                    res_files.remove(file)
                    break
        return FileSet(res_files) if len(res_files) > 0 else None

    def extension_composition(self):
        return Counter([pathlib.Path(file).suffix for file in self.files])

    def dir_sizes(self):
        _dict = {}
        for _dir in self.find_dirs():
            total_size = sum(f.stat().st_size for f in pathlib.Path(_dir).glob('**/*') if f.is_file())
            _dict[_dir] = total_size
        return OrderedDict(sorted(_dict.items(), key=lambda item: item[1], reverse=True))

    def common_root(self):
        min_len, arg_min_len = -1, None
        for file in self.files:
            _len = len(file)
            if _len < min_len or arg_min_len is None:
                min_len = _len
                arg_min_len = file
        return pathlib.Path(arg_min_len).parent


class FileCompressor:
    FILEPATH_SIG = 'FILEPATH_SIG='
    CONTENT_SIG = 'CONTENT_SIG='

    def __init__(self, content):
        self._content = content

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'rb') as f:
            return FileCompressor(f.read())

    @classmethod
    def wrap_file_set(cls, file_set):
        common_root = file_set.common_root()
        res_str = ''
        for file in tqdm(file_set.pathlib_files, desc="Wrap"):
            if file.is_dir():
                continue
            filepath = str(file.relative_to(common_root))
            content = file.read_text(encoding='utf8', errors="ignore")
            res_str += f"{cls.FILEPATH_SIG}{filepath}{cls.CONTENT_SIG}{content}"
        return FileCompressor(res_str)

    @classmethod
    def from_path(cls, path):
        return FileCompressor(FileSet.from_path(path))

    @property
    def size(self):
        return len(self._content)

    @property
    def content(self):
        return self._content

    def encode_and_compress(self):
        self._content = zlib.compress(self._content.encode())
        return self

    def decode_and_decompress(self):
        self._content = zlib.decompress(self._content).decode()
        return self

    def dump(self, filepath):
        with open(filepath, 'wb') as f:
            f.write(self._content)

    def unwrap_to_files(self, _dir):
        dir_path = pathlib.Path(_dir)
        dir_path.mkdir(exist_ok=True)

        if self._content.count(self.FILEPATH_SIG) != self._content.count(self.CONTENT_SIG):
            raise ValueError("Not equal number of FILEPATH_SIG and CONTENT_SIG signatures.")

        split_files = self._content.split(self.FILEPATH_SIG)
        for file in tqdm(split_files, desc="Unwrap"):
            if len(file) == 0:
                continue
            filename, content = file.split(self.CONTENT_SIG)
            file_path = dir_path / pathlib.Path(filename)
            if not file_path.parent.exists():
                for parent in list(file_path.parents)[::-1]:
                    parent.mkdir(exist_ok=True)
            try:
                file_path.write_text(content)
            except Exception as e:
                print(f"File {filename} was skipped because of {e}")

    def __repr__(self):
        return self._content


if __name__ == "__main__":
    p = FileSet.from_path(r"C:\Users\jim\PycharmProjects\python-collection\learning")
    print(f"{p.common_root()=}")
    print(f"{p.dir_sizes()}")

    # filepath = r"C:\Users\jim\PycharmProjects\python-collection\temp.file"
    # c1 = FileCompressor.wrap_file_set(p)
    # print(f"{c1.size=}")
    # c1.encode_and_compress()
    # print(f"{c1.size=}")
    # c1.dump(filepath)
    #
    # c2 = FileCompressor.from_file(filepath)
    # c2.decode_and_decompress()
    # print(f"{c2.size=}")
    # c2.unwrap_to_files(r"C:\Users\jim\PycharmProjects\python-collection\learning_copy")

