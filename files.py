import sys
from os.path import dirname, join


def _project_root() -> str:
    root = dirname(dirname(__file__))
    return join(root, 'ParseRuForms')


def parse_dir() -> str:
    return join(_project_root(), 'to_parse')


def fp_to_parse(fn: str) -> str:
    return join(parse_dir(), fn)


def fp_to_create_tables() -> str:
    return join(_project_root(), 'sql', 'create_tables.sql')


def file_endloc(fh) -> int:
    fh.seek(0, 2)  # Jumps to the end
    endloc = fh.tell()  # Give you the end location (characters from start)
    fh.seek(0)  # Jump to the beginning of the file again
    return endloc
