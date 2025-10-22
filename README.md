# my_wallpapers

A lightweight Python script for managing wallpapers on Hyprland desktops, using either swaybg or hyprpaper.
Easily shift wallpapers or set random ones across multiple monitors.

## Overview

This tool automates wallpaper management for Wayland compositors. It caches your wallpaper directory for fast loading, supports preloading for performance, and
handles multi-monitor setups seamlessly. Designed for simplicity and efficiency with minimal dependencies.

### Features

- Random Mode: Assign random wallpapers to each monitor
- Switch Mode: Cycle through active wallpapers across monitors
- Caching: Avoids rescanning wallpaper directories on every run
- Preloading: Loads wallpapers into memory for instant switching (hyprpaper only)
- Multi-Monitor Support: Automatically detects and configures all connected monitors
- Engine Agnostic: Works with hyprpaper (Hyprland) or swaybg (Sway)

### Requirements

- Python 3.8+
- pgrep (listed in requirements.txt)
- Either hyprpaper (for Hyprland) or swaybg (for Sway)

Install dependencies:

```pip install -r requirements.txt```

## How to Use

### Basic Usage

#### Run the script with one function option and one engine option

```python3 my_wallpaper.py <function> <engine>```

- Functions:
  - switch: Cycle wallpapers across monitors (shifts each monitor's wallpaper to the next)
  - random: Assign random wallpapers to each monitor
- Engines:
  - hyprpaper: For Hyprland desktop environment
  - swaybg: For Sway window manager

### Examples

```python3 my_wallpaper.py random hyprpaper```

```python3 my_wallpaper.py switch swaybg```

### Configuration

The script uses default paths that you can customize by editing variables in the source files (see [Modules](#modules) section below).

- Wallpaper Directory: Defaults to ```~/Wallpapers```
- Cache File: Defaults to ```~/custom/cache/my_wallpaper.json```
- Log File: Defaults to ```~/custom/logs/wallpaper.log```

Ensure these directories exist or modify the paths in the code.

### Logging

All operations are logged to ```~/custom/logs/wallpaper.log``` with timestamps. Check this file for debugging or monitoring.

## Modules

### ```my_wallpaper.py``` (Main Entry Point)

The core script that orchestrates wallpaper management.

Functions:

- ```preload_wallpapers(engine, wallpapers)```: Preloads wallpapers if the engine requires it (e.g., hyprpaper)
- ```wait_engine(engine)```: Waits for the wallpaper engine to be available
- ```get_monitor_names()```: Retrieves and logs monitor names
- ```list_or_cache_wallpapers(cache)```: Loads wallpapers from cache or scans directory
- ```choose_wallpapers(n, cache)```: Selects random wallpapers and updates cache
- ```set_wallpapers(engine, monitors, wallpapers)```: Sets wallpapers for each monitor
- ```random_wallpapers(engine)```: Full random wallpaper workflow
- ```switch_wallpapers(engine)```: Cycles active wallpapers
- ```main(options)```: Parses options and executes the appropriate function

### arguments.py

Handles command-line argument parsing and validation.

Functions:

- ```are_options_valid(options)```: Validates that exactly one function and one engine are selected
- ```make_options(args)```: Converts command-line args to a set of options
- ```get_cmd_args()```: Retrieves and validates command-line arguments

Configuration Variables:

- ```FUNCTION_OPTIONS```: Set of allowed functions (```{'switch', 'random'}```)
- ```ENGINE_OPTION```: Set of allowed engines (```{'hyprpaper', 'swaybg'}```)
- ```POSSIBLE_OPTIONS```: Union of the above sets

### monitors.py

Interfaces with hyprctl to get monitor information.

Functions:

- ```get_monitors()```: Runs ```hyprctl monitors -j``` and parses JSON output
- ```get_monitor_name(monitor)```: Extracts the name from a monitor dict

### wallpaperslib.py

Manages wallpaper file discovery and filtering.

Functions:

- ```last_modified(dir)```: Gets the last modification time of the wallpaper directory
- ```filter_exts(paths, exts)```: Filters paths by file extensions
- ```list_wallpapers(dir)```: Recursively lists image files in the directory

Configuration Variables:

- ```DEFAULT_WALLPAPER_DIR```: Default path to wallpaper directory (currently ```"~/Wallpapers"```)
- ```DEFAULT_IMAGE_EXTENSIONS```: List of supported image extensions (currently ```['.png', '.jpg']```)

### mycache.py

Provides caching functionality for wallpaper lists.

Methods:

- ```Cache.__init__(path)```: Initializes cache with a file path
- ```Cache.load()```: Loads cached data from JSON file
- ```Cache.save(data)```: Saves data to JSON file atomically

Configuration Variables:

- ```DEFAULT_CACHE_FILE```: Default cache file path (currently ```~/custom/cache/my_wallpaper.json```)

### wallpaper_engine.py

Abstract base class defining the interface for wallpaper engines.

Methods (Abstract):

- ```is_callable()```: Checks if the engine is available
- ```needs_to_preload()```: Whether wallpapers need preloading
- ```listloaded()```: Lists preloaded wallpapers
- ```preload(wallpaper)```: Preloads a wallpaper
- ```listactive()```: Lists currently active wallpapers per monitor
- ```wallpaper(monitor_name, wallpaper_path)```: Sets wallpaper for a monitor

### hyprpaper.py

Implementation of WallpaperEngine for hyprpaper.

- Uses ```hyprctl hyprpaper``` commands for wallpaper management
- Require preloading
- Supports active wallpaper listing

Configuration Variables:

- ```HYPRPAPER_CMD```: Base command for hyprpaper (currently "hyprctl hyprpaper")

### swaybg.py

Implementation of WallpaperEngine for swaybg.

- Tracks active wallpapers/swaybg processes in a JSON file
- Does not require preloading; kills old swaybg instances when setting new wallpapers

Configuration Variables:

- ```SWAYBG_CMD```: Command for swaybg (currently "swaybg")
- ```SWAYBG_DATA_FILE```: Path to temporary JSON file for tracking wallpapers and swaybg instances (currently in temp dir)

## License

MIT License - see LICENSE for details.

## Contributing

This is a personal script, but feel free to fork and modify. Ensure any changes maintain compatibility with the abstract engine interface.

<sup><sup>didn't write any of this. Thanks, AI, for existing.</sup></sup>
