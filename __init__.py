import logging
from pathlib import Path

logger = logging.getLogger("attila")

ATTILA_ROOT: Path = Path(__file__).resolve().parent


def get_path() -> str:
    """Returns installation path of the theme.

    Used in ``pelicanconf.py`` to dynamiccaly fetch theme location on the system.
    """
    return str(ATTILA_ROOT)
