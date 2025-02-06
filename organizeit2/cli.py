from rich.console import Console
from rich.table import Table
from typer import Exit, Typer

from organizeit2 import Directory, File


def _unmatched_table(unmatch):
    table = Table(title="Unmatched")
    table.add_column("Path", style="cyan")
    for _ in unmatch:
        table.add_row(str(_))
    console = Console()
    console.print(table)


def match(directory_or_file: str, pattern: str, *, name_only: bool = True, invert: bool = False) -> bool:
    p = File(path=directory_or_file)
    ret = p.resolve().match(pattern, name_only=name_only, invert=invert)
    raise Exit(1 - int(ret))


def all_match(directory: str, pattern: str, *, name_only: bool = True, invert: bool = False) -> bool:
    p = Directory(path=directory).resolve()
    if not isinstance(p, Directory):
        raise Exit(1)
    unmatch = [_ for _ in p.ls() if not _.match(pattern, name_only=name_only, invert=invert)]
    if unmatch:
        _unmatched_table(unmatch)
    raise Exit(min(len(unmatch), 1))


def rematch(directory_or_file: str, pattern: str, *, name_only: bool = True, invert: bool = False) -> bool:
    p = File(path=directory_or_file)
    ret = p.resolve().rematch(pattern, name_only=name_only, invert=invert)
    raise Exit(1 - int(ret))


def all_rematch(directory: str, pattern: str, *, name_only: bool = True, invert: bool = False) -> bool:
    p = Directory(path=directory).resolve()
    if not isinstance(p, Directory):
        raise Exit(1)
    unmatch = [_ for _ in p.ls() if not _.rematch(pattern, name_only=name_only, invert=invert)]
    if unmatch:
        _unmatched_table(unmatch)
    raise Exit(min(len(unmatch), 1))


def main(_test: bool = False):
    app = Typer()
    app.command("match")(match)
    app.command("all-match")(all_match)
    app.command("rematch")(rematch)
    app.command("all-rematch")(all_rematch)
    if _test:
        return app
    return app()


if __name__ == "__main__":
    main()
