from pathlib import Path

from fsspec import AbstractFileSystem

from organizeit2 import Directory, DirectoryPath, OrganizeIt


class TestTypes:
    def test_oit2(self, tempdir):
        oi = OrganizeIt(fs=f"local://{tempdir}")
        assert str(oi.expand("/tmp")) == "file:///tmp"

    def test_directory(self):
        d = Directory(path="local:///tmp")
        assert isinstance(d.path.fs, AbstractFileSystem)
        assert isinstance(d.path.path, Path)
        assert d.model_dump_json() == '{"path":"file:///tmp","type_":"organizeit2.types.Directory"}'
        assert repr(d) == "Directory(path=file:///tmp)"
        assert str(d) == "file:///tmp"
        assert str(d.path) == "file:///tmp"

    def test_directory_from_directorypath(self):
        Directory(path=DirectoryPath("local:///tmp"))

    def test_directory_ls(self, directory_str):
        d = Directory(path=directory_str)
        root = str(d)
        assert [str(_) for _ in d.ls()] == [
            f"{root}/subdir1",
            f"{root}/subdir2",
            f"{root}/subdir3",
            f"{root}/subdir4",
        ]

    def test_directory_recurse(self, directory_str):
        d = Directory(path=directory_str)
        assert len([str(_) for _ in d.recurse()]) == 64

    # TODO
    # def test_directory_list(self, directory_str):
    #     d = Directory(path=directory_str)
    #     assert d.list() == []
