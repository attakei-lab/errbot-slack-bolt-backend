from pathlib import Path


def get_plugin_dir() -> Path:
    """
        Create path for directory of itself
        ===================================

        You can use if you install plugin as package, and set ``BOT_EXTRA_BACKEND_DIR``.

        :return: Path object of plugin directory
    """
    return Path(__file__).parent
