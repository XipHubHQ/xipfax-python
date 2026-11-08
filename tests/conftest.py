"""Strips every variable shaped like a credential, or named for XipFax, from the environment as the
specs load, before any of them is collected, so that no spec has a key from the shell to reach the
API with."""

from tests import credentials

credentials.strip()
