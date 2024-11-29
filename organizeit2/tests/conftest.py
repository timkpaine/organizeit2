from tempfile import TemporaryDirectory

from pytest import fixture


@fixture(scope="module", autouse=True)
def tempdir():
    with TemporaryDirectory() as td:
        yield td


@fixture(scope="module", autouse=True)
def directory_str():
    return "file://organizeit2/tests/directory"
