from tempfile import TemporaryDirectory

from pytest import fixture


@fixture(scope="module", autouse=True)
def tempdir():
    with TemporaryDirectory() as td:
        yield td
