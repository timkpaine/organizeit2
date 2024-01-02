import pydantic
from packaging.version import Version

if Version(pydantic.__version__) >= Version("2"):
    from pydantic import SerializeAsAny  # noqa: F401
else:

    class SerializeAsAny:
        def __class_getitem__(self, typ):
            return typ
