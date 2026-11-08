"""Keeps every credential out of the specs. conftest.py strips each before any spec loads: anything
in the environment shaped like a credential, or named for XipFax, goes. The day a real key sits in a
developer's shell, a spec that could reach the API still has nothing to reach it with, and the specs
keep saying so."""

import os
import re
from collections.abc import Mapping

# A variable that is a secret in itself, in any case.
SECRET = re.compile(
    r"TOKEN|SECRET|PASSWORD|CREDENTIAL|AUTH|APIKEY|API_KEY|_KEY\Z|_KEYS\Z|COOKIE|PRIVATE",
    re.IGNORECASE,
)

# The variables XipFax's own examples read, such as XIPFAX_API_KEY.
XIPFAX = re.compile(r"\AXIPFAX_", re.IGNORECASE)


def shaped(name: str) -> bool:
    """Whether a spec's process has no business carrying the variable name."""
    return SECRET.search(name) is not None or XIPFAX.search(name) is not None


def left(environment: Mapping[str, str] | None = None) -> list[str]:
    """The name of each such variable in the environment, the process's unless another is given,
    sorted."""
    names = os.environ if environment is None else environment
    return sorted(name for name in names if shaped(name))


def strip() -> list[str]:
    """Removes each such variable from the process's environment, answering the names it removed,
    sorted."""
    removed = left()
    for name in removed:
        del os.environ[name]
    return removed
