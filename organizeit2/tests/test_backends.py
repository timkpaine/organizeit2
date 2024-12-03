import os

import pytest

from organizeit2 import Directory


class TestBackends:
    @pytest.mark.skipif(os.environ.get("FSSPEC_S3_ENDPOINT_URL") is None, reason="Skipping test that require S3 credentials")
    def test_s3(self):
        d = Directory(path="s3://timkpaine-public/projects/organizeit2")
        root = str(d)
        assert [str(_) for _ in d.ls()] == [
            f"{root}/subdir1",
            f"{root}/subdir2",
            f"{root}/subdir3",
            f"{root}/subdir4",
        ]
        assert len(d.recurse()) == 64
