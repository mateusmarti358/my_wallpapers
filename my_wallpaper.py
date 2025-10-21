from hyprpaper import HyprPaper
from pathlib import Path
import time
import logging

import arguments
from monitors import get_monitors, get_monitor_name
import wallpaperslib
import random
import mycache


def preload_wallpapers(hpaper: HyprPaper, wallpapers: list[Path]):
    all_loaded = hpaper.listloaded()

    logging.info("Loaded Wallpapers: ")
    for loaded in all_loaded:
        if loaded == "":
            all_loaded.remove(loaded)
            continue
        logging.info(loaded)

    are_all_loaded = True

    for wallpaper in wallpapers:
        if str(wallpaper) in all_loaded:
            continue
        are_all_loaded = False
        logging.info(f"Loading: {wallpaper}")
        hpaper.preload(wallpaper)

    if are_all_loaded:
        logging.info("All wallpapers are loaded")


def wait_hyprpaper():
    hpaper = HyprPaper()

    if not hpaper.is_running():
        time.sleep(0)
        while not hpaper.is_running():
            logging.info(f"Waiting Hyprpaper start")
            time.sleep(0)

    return hpaper


def get_monitor_names():
    monitors = get_monitors()
    monitor_names = [get_monitor_name(monitor) for monitor in monitors]

    logging.info("Monitors: ")
    for name in monitor_names:
        logging.info(name)
    logging.info("")

    return monitor_names


def list_or_cache_wallpapers(cache: mycache.Cache):
    wallpapers_last_mod = wallpaperslib.last_modified()
    all_wallpapers = []
    cache_data = cache.load()

    if cache_data:
        if cache_data["last_modified"] >= wallpapers_last_mod:
            logging.info("Wallpapers loaded from cache")
            return cache_data["wallpapers"]
        else:
            logging.info("Outdated cache")
    else:
        logging.info("Empty or Invalid cache")

    all_wallpapers = wallpaperslib.list_wallpapers()

    logging.info("Updating cache!")
    cache.save(
        {
            "last_modified": wallpapers_last_mod,
            "wallpapers": [str(wallpaper) for wallpaper in all_wallpapers],
        }
    )

    return all_wallpapers


def choose_wallpapers(n: int, cache: mycache.Cache):
    all_wallpapers = list_or_cache_wallpapers(cache)

    chosen_wallpapers = random.sample(all_wallpapers, n)

    out_tuple = (all_wallpapers, chosen_wallpapers)

    logging.info("Wallpapers: ")
    for wp in all_wallpapers:
        logging.info(wp)
    logging.info("")

    return out_tuple


def set_wallpapers(hpaper: HyprPaper, monitors: list[str], wallpapers: list[Path]):
    if len(wallpapers) != len(monitors):
        raise ValueError("Number of monitors and wallpapers must be equal")

    for i in range(len(monitors)):
        monitor = monitors[i]
        wallpaper = wallpapers[i]

        logging.info(f"{monitor}: {wallpaper}")
        hpaper.wallpaper(monitor, wallpaper)


def random_wallpapers():
    monitor_names = get_monitor_names()

    cache = mycache.Cache()
    _, chosen_wallpapers = choose_wallpapers(len(monitor_names), cache)

    hpaper = wait_hyprpaper()

    preload_wallpapers(hpaper, chosen_wallpapers)

    set_wallpapers(hpaper, monitor_names, chosen_wallpapers)


def shift_wallpapers(mn_wp_list: list[tuple[str, str]]):
    wallpapers = [mn_wp[1] for mn_wp in mn_wp_list]
    wallpapers = [wallpapers[-1]] + wallpapers[:-1]

    shifted_list = [
        (mn, wp) for (mn, wp) in zip([mn_wp[0] for mn_wp in mn_wp_list], wallpapers)
    ]

    return shifted_list


def switch_wallpapers():
    hpaper = wait_hyprpaper()

    active_wallpapers = hpaper.listactive()

    shifted_list = shift_wallpapers(active_wallpapers)

    monitor_names = [mn_wp[0] for mn_wp in shifted_list]
    wallpapers = [Path(mn_wp[1]) for mn_wp in shifted_list]

    set_wallpapers(hpaper, monitor_names, wallpapers)


def main(options: set):
    if "switch" in options:
        switch_wallpapers()
        return
    if "random" in options:
        random_wallpapers()
    raise ValueError("No option selected")


if __name__ == "__main__":
    logging.basicConfig(
        filename=Path("~/custom/logs/wallpaper.log").expanduser(),
        level=logging.INFO,
        format="[%(asctime)s]: %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    args = arguments.get_cmd_args()
    options = arguments.make_options(args)

    main(options)

    logging.info("END OK")
