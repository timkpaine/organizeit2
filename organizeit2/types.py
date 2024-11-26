from ccflow import BaseModel

from .fsspec_types import DirectoryPath, FilePath, Path

__all__ = (
    "Directory",
    "File",
)


# TODO: share base with File?
class Directory(BaseModel):
    path: DirectoryPath

    def __repr__(self) -> str:
        return f"Directory(path={str(self.path)})"

    def __str__(self) -> str:
        return str(self.path)

    def __lt__(self, other) -> bool:
        return str(self) < str(other)

    def ls(self):
        # TODO: sort?
        # TODO: make fast for large dirs?

        # this will autoresolve types correctly
        paths = sorted(Path(fs=self.path.fs, path=path) for path in self.path.fs.ls(self.path.path))
        return [Directory(path=path) if path.isdir() else File(path=path) for path in paths]

    def list(self):
        return self.path.fs.listdir(self.path.path)

    def recurse(self):
        # this will autoresolve types correctly
        paths = []
        all = self.ls()
        for file_or_dir in all:
            if file_or_dir.path.isdir():
                paths.extend(file_or_dir.recurse())
            else:
                paths.append(file_or_dir)
        return paths

    def apply(self, foo, include_dir: bool = False, recursive: bool = False): ...


class File(BaseModel):
    path: FilePath

    def __repr__(self) -> str:
        return f"File(path={str(self.path)})"

    def __str__(self) -> str:
        return str(self.path)

    def __lt__(self, other) -> bool:
        return str(self) < str(other)
