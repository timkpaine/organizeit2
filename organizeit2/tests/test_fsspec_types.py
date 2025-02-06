from pathlib import Path as BasePath

from fsspec import AbstractFileSystem

from organizeit2 import BasePath as Path, DirectoryPath, FilePath, FileSystem


class TestFSSpecTypes:
    def test_fs(self):
        fs = FileSystem("local:///tmp")
        assert isinstance(fs, AbstractFileSystem)

    def test_file(self):
        file = FilePath("local:///tmp")
        print(type(file))
        assert isinstance(file, Path)
        assert isinstance(file.fs, AbstractFileSystem)
        assert isinstance(file.path, BasePath)
        assert str(file) == "file:///tmp"

    def test_dir(self):
        dir = DirectoryPath("local:///tmp")
        assert isinstance(dir, Path)
        assert isinstance(dir.fs, AbstractFileSystem)
        assert isinstance(dir.path, BasePath)
        assert str(dir) == "file:///tmp"

    def test_resolve(self):
        dir = Path("local:///tmp")
        assert dir.type == "fsspec-dir"
        file = Path(f"local://{__file__}")
        assert file.type == "fsspec-file"
