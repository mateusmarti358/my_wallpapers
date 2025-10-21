from pathlib import Path
from typing import Iterator

DEFAULT_WALLPAPER_DIR = Path("~/Wallpapers").expanduser()
DEFAULT_IMAGE_EXTENSIONS = ['.png', '.jpg']

def last_modified(dir=DEFAULT_WALLPAPER_DIR):
    return dir.stat().st_mtime

def filter_exts(paths: Iterator[Path], exts: list[str]=DEFAULT_IMAGE_EXTENSIONS):
    return [path for path in paths if path.suffix in exts]

def list_wallpapers(dir=DEFAULT_WALLPAPER_DIR):
    all_files = dir.rglob('*')
    all_images = filter_exts(all_files)
    return all_images
