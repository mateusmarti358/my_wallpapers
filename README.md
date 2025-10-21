# my_wallpapers

A Python script to manage wallpapers for Hyprland using hyprpaper.

## Usage

Run with: python3 my_wallpaper.py <switch|random>

- switch: Cycles wallpapers across monitors.
- random: Assigns random wallpapers to each monitor.

## Modules

- my_wallpaper.py: Main entry point. Handles preloading, setting, and switching wallpapers via hyprpaper.
- arguments.py: Parses CLI args, validates 'switch' or 'random' options.
- monitors.py: Retrieves monitor names using hyprctl monitors.
- wallpapers.py: Scans ~/Wallpapers for .png/.jpg files, tracks last modified time.
- mycache.py: Caches wallpaper list in ~/custom/cache/my_wallpaper.json to avoid rescanning.
- hyprpaper.py: Interfaces with hyprpaper daemon via hyprctl hyprpaper commands (preload, listloaded, listactive, wallpaper).

## System Interaction

Interacts with Hyprland's hyprpaper daemon through hyprctl subprocess calls. Preloads wallpapers into memory, sets per-monitor wallpapers, and waits for hyprpaper to start if needed. Uses pgrep to check daemon status. Logs to ~/custom/logs/wallpaper.log.

## Dependencies

• pgrep (via pip: pgrep==2020.12.3)
• hyprpaper running in Hyprland environment.