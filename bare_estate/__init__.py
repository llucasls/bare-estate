from importlib.metadata import version


__version__: str | None
try:
    __version__ = version("bare_estate")
except ModuleNotFoundError:
    __version__ = None
