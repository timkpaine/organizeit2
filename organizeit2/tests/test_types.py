from os import getcwd
from pathlib import Path

from fsspec import AbstractFileSystem

from organizeit2 import Directory, OrganizeIt


class TestTypes:
    def test_oit2(self, tempdir):
        oi = OrganizeIt(fs=f"local://{tempdir}")
        assert oi.expand("/tmp")

    def test_directory(self):
        d = Directory(path="local:///tmp")
        assert isinstance(d.path.fs, AbstractFileSystem)
        assert isinstance(d.path.path, Path)
        assert d.model_dump_json() == '{"path":"file:///tmp","type_":"organizeit2.types.Directory"}'
        assert str(d) == f"Directory(path=DirectoryPath(fs=file://{getcwd()}, path=/tmp))"
        assert str(d.path) == "file:///tmp"
