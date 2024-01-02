from omegaconf import DictConfig, OmegaConf
from pathlib import Path
from pydantic import Field, validator
from typing import Dict, Union

from .base import BaseModel
from .utils import SerializeAsAny


class Configuration(BaseModel):
    resources: Dict[str, SerializeAsAny[BaseModel]] = Field(default_factory=dict)
    # content: List[SerializeAsAny[Content]] = Field(default_factory=list)

    @validator("resources", pre=True)
    def convert_resources_from_obj(cls, value):
        if value is None:
            value = {}
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = BaseModel._to_type(v)
        return value
    """
    @validator("content", pre=True)
    def convert_content_from_obj(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            for i, element in enumerate(v):
                if isinstance(element, str):
                    v[i] = Content(type=Type.from_string(element))
                elif isinstance(element, dict):
                    v[i] = BaseModel._to_type(element)
        return v
    """

def load(path_or_model: Union[str, Path, dict, Configuration]) -> Configuration:
    if isinstance(path_or_model, Configuration):
        return path_or_model

    if isinstance(path_or_model, str) and (
        path_or_model.endswith(".yml") or path_or_model.endswith(".yaml") or path_or_model.endswith(".zorp")
    ):
        path_or_model = Path(path_or_model).resolve()

    if isinstance(path_or_model, Path):
        path_or_model = OmegaConf.load(path_or_model)

    if isinstance(path_or_model, DictConfig):
        container = OmegaConf.to_container(path_or_model, resolve=True, throw_on_missing=True)
        return Configuration(**container)

    raise TypeError(f"Path or model malformed: {path_or_model} {type(path_or_model)}")
