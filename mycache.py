import tempfile
import os, json, time
from pathlib import Path
from typing import Any, Dict, Optional

# ik I can use .cache, but I want to keep it simple for me
DEFAULT_CACHE_FILE = Path('~/custom/cache/my_wallpaper.json').expanduser()

class Cache:
    def __init__(self, path: Path = DEFAULT_CACHE_FILE):
        self.path = path.expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Optional[Dict[str, Any]]:
        try:
            if not self.path.exists():
                return None
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def save(self, data: Dict[str, Any]) -> None:
        dirpath = self.path.parent
        with tempfile.NamedTemporaryFile("w", delete=False, dir=str(dirpath), encoding="utf-8") as tf:
            json.dump(data, tf, ensure_ascii=False)
            tf.flush()
            os.fsync(tf.fileno())
            tmpname = tf.name
        os.replace(tmpname, str(self.path))
