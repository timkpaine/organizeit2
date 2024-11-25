from dataclasses import dataclass
from pathlib import Path as BasePath
from typing import Any, Optional, Union

from fsspec import get_fs_token_paths
from fsspec.implementations.local import AbstractFileSystem
from pydantic.annotated_handlers import GetCoreSchemaHandler
from pydantic.json_schema import GetJsonSchemaHandler, JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core.core_schema import any_schema, no_info_after_validator_function, plain_serializer_function_ser_schema, str_schema
from typing_extensions import Annotated, Literal

__all__ = (
    "FileSystem",
    "Path",
    "FilePath",
    "DirectoryPath",
)


@dataclass
class FSSpecFilesystemType:
    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> CoreSchema:
        assert isinstance(source, type) and issubclass(source, AbstractFileSystem)
        return no_info_after_validator_function(
            cls._validate,
            any_schema(),
            serialization=plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=any_schema(),
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        field_schema.update(format="fsspec-fs", type="string")
        return field_schema

    @staticmethod
    def _validate(value: Union[AbstractFileSystem, str]) -> "FSSpecFilesystemType":
        if isinstance(value, AbstractFileSystem):
            return value
        fs, _, _ = get_fs_token_paths(value)
        return fs

    @staticmethod
    def _serialize(value: "FSSpecFilesystemType") -> str:
        return value.unstrip_protocol("")


FileSystem = Annotated[AbstractFileSystem, FSSpecFilesystemType]
PathType = Literal["fsspec-file", "fsspec-dir"]


@dataclass
class Path:
    fs: FileSystem
    path: BasePath
    type: PathType

    def __init__(self, fs: Union[AbstractFileSystem, str], path: Optional[BasePath] = None, type: PathType = None) -> "Path":
        if isinstance(fs, str):
            self.fs, _, paths = get_fs_token_paths(fs)
            self.path = BasePath(paths[0])
            if self.fs.isdir(paths[0]):
                self.type = "fsspec-dir"
            else:
                self.type = "fsspec-file"
        else:
            self.fs = fs
            self.path = path
            self.type = type

    def __repr__(self) -> str:
        return f"{'DirectoryPath' if self.type == 'fsspec-dir' else 'FilePath'}(fs={self.fs.unstrip_protocol('')}, path={str(self.path)})"

    def __str__(self) -> str:
        return self.fs.unstrip_protocol(self.path.as_posix())


@dataclass
class FSSpecPathType:
    path_type: PathType

    def __get_pydantic_core_schema__(self, source: type[Any], handler: GetCoreSchemaHandler) -> CoreSchema:
        assert source is Path
        return no_info_after_validator_function(
            self._validate_file if self.path_type == "fsspec-file" else self._validate_dir,
            str_schema(),
            serialization=plain_serializer_function_ser_schema(
                self._serialize,
                info_arg=False,
                return_schema=str_schema(),
            ),
        )

    def __get_pydantic_json_schema__(self, core_schema: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        format_conversion = {"fsspec-file": "file-path", "fsspec-dir": "directory-path"}
        field_schema.update(format=format_conversion[self.path_type], type="string")
        return field_schema

    @staticmethod
    def _validate_dir(value: str, _raise: bool = True) -> "Path":
        fs, _, paths = get_fs_token_paths(value)
        if not fs.isdir(paths[0]) and _raise:
            raise ValueError("Not a dir")
        return Path(fs, BasePath(paths[0]), "fsspec-dir")

    @staticmethod
    def _validate_file(value: str, _raise: bool = True) -> "Path":
        fs, _, paths = get_fs_token_paths(value)
        if not fs.isfile(paths[0]) and _raise:
            raise ValueError("Not a file")
        return Path(fs, BasePath(paths[0]), "fsspec-file")

    @staticmethod
    def _serialize(value: "Path") -> str:
        return str(value)


FilePath = Annotated[Path, FSSpecPathType(path_type="file")]
DirectoryPath = Annotated[Path, FSSpecPathType(path_type="dir")]