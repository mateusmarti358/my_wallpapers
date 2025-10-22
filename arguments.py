import sys

FUNCTION_OPTIONS = {'switch', 'random'}
ENGINE_OPTION = { 'hyprpaper', 'swaybg' }
POSSIBLE_OPTIONS = FUNCTION_OPTIONS | ENGINE_OPTION

def are_options_valid(options):
    function_selected = 0
    engine_selected = 0

    for arg in options:
        if arg in FUNCTION_OPTIONS:
            function_selected += 1
            continue
        if arg in ENGINE_OPTION:
            engine_selected += 1
            continue
        return False
    
    return function_selected == 1 and engine_selected == 1

def make_options(args):
    options = set()

    for arg in args:
        if arg not in POSSIBLE_OPTIONS:
            raise ValueError(f"Unknown option: {arg}")
        options.add(arg)
    
    if not are_options_valid(options):
        raise ValueError("Invalid options selected")
    return options

def get_cmd_args():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <switch>")
        sys.exit(1)
        
    return sys.argv[1:]