from typing import Tuple
import pgrep
import os
import subprocess

from wallpaper_engine import WallpaperEngine

HYPRPAPER_CMD = "hyprctl hyprpaper"


class HyprPaper(WallpaperEngine):
    def is_running(self) -> bool:
        return len(pgrep.pgrep("hyprpaper")) != 0

    def needs_to_preload(self) -> bool:
        return True

    def listloaded(self) -> list[str]:
        if not self.is_running():
            return []
        cmd = ["hyprctl", "hyprpaper", "listloaded"]
        out = subprocess.run(cmd, capture_output=True).stdout.decode("utf-8")
        return str(out).split("\n")

    def listactive(self) -> list[Tuple[str, str]]:
        if not self.is_running():
            return []
        cmd = ["hyprctl", "hyprpaper", "listactive"]

        activeres = subprocess.run(cmd, capture_output=True).stdout.decode("utf-8")
        activeres = str(activeres).split("\n")
        activeres = [res for res in activeres if res != ""]

        out = []

        for i in range(len(activeres)):
            [monitor_name, wallpaper] = activeres[i].split("=")
            monitor_name = monitor_name.strip()
            wallpaper = wallpaper.strip()
            out.append((monitor_name, wallpaper))

        return out

    def preload(self, wallpaper):
        if not self.is_running():
            return None
        preload_cmd = f"{HYPRPAPER_CMD} preload {wallpaper}"
        os.system(preload_cmd)

    def wallpaper(self, monitor_name, wallpaper_path):
        if not self.is_running():
            return None
        mon_wpp_str = f'"{monitor_name},{wallpaper_path}"'
        setwallpaper_cmd = f"{HYPRPAPER_CMD} wallpaper {mon_wpp_str}"
        os.system(setwallpaper_cmd)
