import argparse
from typing import Any, Dict, List, NamedTuple, Optional, Union

from httpie.cli.argtypes import PARSED_DEFAULT_FORMAT_OPTIONS
from httpie.cli.constants import (PRETTY_MAP, PRETTY_STDOUT_TTY_ONLY,
                                  PrettyOptions)
from httpie.context import Environment
from httpie.output.formatters.colors import AUTO_STYLE


class ProcessingOptions(NamedTuple):
    """Represents a set of stylistic options
    that are used when deciding which stream
    should be used.
    """

    debug: bool = False
    traceback: bool = False

    stream: bool = False
    style: str = AUTO_STYLE
    prettify: Union[List[str], PrettyOptions] = PRETTY_STDOUT_TTY_ONLY

    response_mime: Optional[str] = None
    response_charset: Optional[str] = None

    json: bool = False
    format_options: Dict[str, Any] = PARSED_DEFAULT_FORMAT_OPTIONS

    def get_prettify(self, env: Environment) -> List[str]:
        if self.prettify is PRETTY_STDOUT_TTY_ONLY:
            return PRETTY_MAP['all' if env.stdout_isatty else 'none']
        else:
            return self.prettify

    @classmethod
    def from_raw_args(cls, options: argparse.Namespace) -> 'ProcessingOptions':
        fetched_options = {
            option: getattr(options, option)
            for option in cls._fields
        }
        return cls(**fetched_options)

    @property
    def show_traceback(self):
        return self.debug or self.traceback
