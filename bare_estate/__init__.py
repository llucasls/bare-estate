from importlib.metadata import version


try:
    __version__ = version("bare_estate")
except ModuleNotFoundError:
    __version__ = None
