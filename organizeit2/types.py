from ccflow import BaseModel
from fsspec.implementations.local import LocalFileSystem
from pydantic import Field

from .fsspec_types import DirectoryPath, FilePath, FileSystem


class Directory(BaseModel):
    path: DirectoryPath

    def list(self):
        pass

    def recurse(self): ...
    def apply(self, foo, include_dir: bool = False, recursive: bool = False): ...


class File(BaseModel):
    path: FilePath


# TODO: inherit from directory?
class OrganizeIt(BaseModel):
    fs: FileSystem = Field(default_factory=LocalFileSystem)

    def expand(self, directory) -> Directory:
        return Directory(path=self.fs.unstrip_protocol(directory))
