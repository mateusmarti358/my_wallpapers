import pgrep
import subprocess
import tempfile
import os
import atexit

import json

from wallpaper_engine import WallpaperEngine

SWAYBG_CMD = "swaybg"
SWAYBG_DATA_FILE = os.path.join(tempfile.gettempdir(), "swaybg_state.json")

class Swaybg(WallpaperEngine):
    def __init__(self) -> None:
        super().__init__()
        
        self.data = {}
        atexit.register(self.save)

        if not os.path.exists(SWAYBG_DATA_FILE):
            with open(SWAYBG_DATA_FILE, "w") as f:
                json.dump(self.data, f)
                return

        with open(SWAYBG_DATA_FILE, "r") as f:
            try: self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = {}

    def save(self):
        with open(SWAYBG_DATA_FILE, "w") as f:
            json.dump(self.data, f)

    def is_callable(self) -> bool:
        return True

    def needs_to_preload(self) -> bool:
        return False
    
    def listloaded(self) -> list[str]:
        return []

    def preload(self, wallpaper):
        return

    def listactive(self) -> list[tuple[str, str]]:
        active_wallpapers = []
        for [_pid, active_monitor_wallpaper] in self.data.items():
            monitor = active_monitor_wallpaper["monitor"]
            wallpaper = active_monitor_wallpaper["wallpaper"]
            active_wallpapers.append((monitor, wallpaper))
        return active_wallpapers

    def kill_inst_with_monitor(self, monitor_name):
        removed_pid = None
        for [pid, active_monitor_wallpaper] in self.data.items():
            if active_monitor_wallpaper["monitor"] == monitor_name:
                try: os.kill(int(pid), 9)
                except: pass
                removed_pid = pid

        if removed_pid:
            del self.data[removed_pid]

        self.save()

    def wallpaper(self, monitor_name, wallpaper_path):
        self.kill_inst_with_monitor(monitor_name)

        mon_wpp_str = f'-o {monitor_name} -i {wallpaper_path}'
        setwallpaper_cmd = f'{SWAYBG_CMD} {mon_wpp_str}'
        proc = subprocess.Popen(setwallpaper_cmd.split(' '))

        self.data[proc.pid] = {
            "monitor": monitor_name,
            "wallpaper": str(wallpaper_path)
        }

        self.save()
