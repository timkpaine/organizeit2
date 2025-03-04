from rich.console import Console
from rich.table import Table
from typer import Exit, Option, Typer
from typing_extensions import Annotated

from organizeit2 import Directory


def _unmatched_table(unmatch):
    if unmatch:
        table = Table(title="Unmatched")
        table.add_column("Path", style="cyan")
        for _ in unmatch:
            table.add_row(str(_))
        console = Console()
        console.print(table)
    else:
        print("All matched")


def match(
    directory: str,
    pattern: str,
    *,
    list: Annotated[bool, Option("--list/--no-list", "-l/-L")] = False,
    name_only: Annotated[bool, Option("--name-only/--no-name-only", "-n/-N")] = True,
    invert: Annotated[bool, Option("--invert/--no-invert", "-i/-I")] = False,
) -> bool:
    p = Directory(path=directory).resolve()
    if not isinstance(p, Directory) or not directory.endswith("/"):
        matched = [p] if p.resolve().match(pattern, name_only=name_only, invert=invert) else []
        all = [] if matched else [p]
    else:
        matched = p.all_match(pattern, name_only=name_only, invert=invert)
        all = p.ls()
    intersection = set(all) - set(matched)
    if list:
        for _ in intersection:
            print(_.as_posix())
    else:
        _unmatched_table(intersection)
    raise Exit(min(len(intersection), 1))


def rematch(
    directory: str,
    pattern: str,
    *,
    list: Annotated[bool, Option("--list/--no-list", "-l/-L")] = False,
    name_only: Annotated[bool, Option("--name-only/--no-name-only", "-n/-N")] = True,
    invert: Annotated[bool, Option("--invert/--no-invert", "-i/-I")] = False,
) -> bool:
    p = Directory(path=directory).resolve()
    if not isinstance(p, Directory) or not directory.endswith("/"):
        matched = [p] if p.resolve().rematch(pattern, name_only=name_only, invert=invert) else []
        all = [] if matched else [p]
    else:
        matched = p.all_rematch(pattern, name_only=name_only, invert=invert)
        all = p.ls()

    # calculate the overlap
    intersection = set(all) - set(matched)

    # return code means everything looked for was matched
    return_code = 0 if not intersection else 1
    if list:
        for _ in intersection:
            print(_.as_posix())
    else:
        _unmatched_table(intersection)
    raise Exit(return_code)


def main(_test: bool = False):
    app = Typer()
    app.command("match")(match)
    app.command("all-match")(match)
    app.command("rematch")(rematch)
    app.command("all-rematch")(rematch)
    if _test:
        return app
    return app()


if __name__ == "__main__":
    main()
