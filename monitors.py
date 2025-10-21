import subprocess
import json

def get_monitors():
    cmd = ['hyprctl', 'monitors', '-j']
    out = subprocess.run(cmd, capture_output=True).stdout
    json_out = json.loads(out)
    return json_out


def get_monitor_name(monitor):
    return monitor['name']
