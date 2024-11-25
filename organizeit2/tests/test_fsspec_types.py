from pathlib import Path as BasePath

from fsspec import AbstractFileSystem

from organizeit2 import DirectoryPath, FilePath, FileSystem, Path


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
        print(type(dir))
        assert isinstance(dir, Path)
        assert isinstance(dir.fs, AbstractFileSystem)
        assert isinstance(dir.path, BasePath)
        assert str(dir) == "file:///tmp"
