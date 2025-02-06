from unittest.mock import patch

from typer.testing import CliRunner

from organizeit2.cli import main

runner = CliRunner()


def test_app_match(directory_str):
    app = main(_test=True)
    assert runner.invoke(app, ["match", str(directory_str), "directory*"]).exit_code == 0
    assert runner.invoke(app, ["match", str(directory_str), "directory*", "--invert"]).exit_code == 1
    assert runner.invoke(app, ["match", str(directory_str), "directory", "--no-name-only"]).exit_code == 1
    assert runner.invoke(app, ["match", str(directory_str), "directory", "--no-name-only", "--invert"]).exit_code == 0
    assert runner.invoke(app, ["match", str(directory_str), "*organizeit2*directory", "--no-name-only"]).exit_code == 0
    assert runner.invoke(app, ["match", str(directory_str), "*organizeit2*directory", "--no-name-only", "--invert"]).exit_code == 1


def test_app_all_match(directory_str):
    app = main(_test=True)
    assert runner.invoke(app, ["all-match", str(directory_str), "subdir*"]).exit_code == 0
    assert runner.invoke(app, ["all-match", str(directory_str), "dir*"]).exit_code == 1

    with patch("organizeit2.cli.print") as print_mock:
        assert runner.invoke(app, ["all-match", str(directory_str), "subdir*", "--list"]).exit_code == 0
        assert print_mock.call_count == 4


def test_app_rematch(directory_str):
    app = main(_test=True)
    assert runner.invoke(app, ["rematch", str(directory_str), "directory"]).exit_code == 0
    assert runner.invoke(app, ["rematch", str(directory_str), "directory", "--invert"]).exit_code == 1
    assert runner.invoke(app, ["rematch", str(directory_str), "directory", "--no-name-only"]).exit_code == 1
    assert runner.invoke(app, ["rematch", str(directory_str), "directory", "--no-name-only", "--invert"]).exit_code == 0
    assert runner.invoke(app, ["rematch", str(directory_str), "file://[a-zA-Z0-9/]*", "--no-name-only"]).exit_code == 0


def test_app_all_rematch(directory_str):
    app = main(_test=True)
    assert runner.invoke(app, ["all-rematch", str(directory_str), "subdir[0-9]+"]).exit_code == 0
    assert runner.invoke(app, ["all-rematch", str(directory_str), "subdir[0-3]+"]).exit_code == 1

    with patch("organizeit2.cli.print") as print_mock:
        assert runner.invoke(app, ["all-rematch", str(directory_str), "subdir*", "--list"]).exit_code == 0
        assert print_mock.call_count == 4
