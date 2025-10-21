import sys

POSSIBLE_OPTIONS = {'switch', 'random'}

def make_options(args):
    options = set()

    for arg in args:
        if arg not in POSSIBLE_OPTIONS:
            raise ValueError(f"Unknown option: {arg}")
        
        if arg in options:
            raise ValueError("random option already set")
        options.add(arg)
    
    return options

def get_cmd_args():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <switch>")
        sys.exit(1)
        
    return sys.argv[1:]