from importlib import import_module
from json import loads
from pydantic import BaseModel, validator
from typing import Optional, Type

from .utils import SerializeAsAny


class Type(BaseModel):
    module: str
    name: str

    @classmethod
    def from_string(cls, str: str) -> "Type":
        module, name = str.split(":")
        return Type(module=module, name=name)

    def to_string(self) -> str:
        return f"{self.module}:{self.name}"

    def type(self) -> Type["Type"]:
        return getattr(import_module(self.module), self.name)

    def load(self, **kwargs) -> "Type":
        return self.type()(**kwargs)


class BaseModel(BaseModel):
    type: SerializeAsAny[Type]

    # internals
    _nb_var_name: Optional[str] = ""

    class Config:
        arbitrary_types_allowed: bool = False
        extra: str = "ignore"
        validate_assignment: bool = True

    def __init__(self, **kwargs):
        if "type" not in kwargs:
            kwargs["type"] = Type(module=self.__class__.__module__, name=self.__class__.__name__)
        super().__init__(**kwargs)

    @validator("type", pre=True)
    def convert_type_string_to_module_and_name(cls, v):
        if isinstance(v, str):
            return Type.from_string(v)
        return v

    @staticmethod
    def _to_type(value, model_type=None):
        if value is None:
            value = {}

        if model_type is None and "type" in value:
            # derive type from instantiation
            model_type = BaseModel

        if isinstance(value, dict):
            return model_type(**value).type.load(**value)

        return value

    @classmethod
    def from_json(cls, json):
        data = loads(json)
        return cls(**data)

    def __repr__(self) -> str:
        # Truncate the output for now
        return f"<{self.__class__.__name__}>"
