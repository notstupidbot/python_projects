#!/usr/bin/env python3
import json
import sys
import importlib.util

import os

def get_current_script_directory():
    # Get the absolute path of the current Python script
    current_script_path = os.path.abspath(__file__)

    # Extract the directory from the script path
    script_directory = os.path.dirname(current_script_path)

    return script_directory

# sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))
artisan_dir="%s/artisan" % get_current_script_directory()
action_json_path="%s/actions.json" % artisan_dir

with open(action_json_path) as f:
    config = json.load(f)
    availables = config["availables"]

# Import action modules
def import_action_modules(availables):
    module_actions = {}
    for action in availables:
        try:
            spec = importlib.util.spec_from_file_location(action, f"{artisan_dir}/{action}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module_actions[action] = module
        except ImportError:
            print(f"Failed to import action module: {action}")
    return module_actions

# Show help for available actions
def show_help(availables):
    print("Available actions:")
    for action in availables:
        print(f"- {action}")

# Get action arguments from command-line arguments
def get_action_args(args):
    if len(args) >= 2:
        return args[1]
    return None

# Process the action
def process_action(action_name, args, module_actions, availables):
    if action_name in availables:
        module = module_actions.get(action_name)
        if module:
            # print(args)
            args.pop(0)
            args.pop(0)
            # args.pop()
            module.main(*args)
        else:
            print(f"Action module '{action_name}' not found.")
    else:
        print(f"Action '{action_name}' not available.")
def call_dynamic_function(func, *args, **kwargs):
    return func(*args, **kwargs)

def main():
    argv = sys.argv
    module_actions = import_action_modules(availables)
    action_name = get_action_args(argv)

    if action_name:
        process_action(action_name, argv, module_actions, availables)
    else:
        show_help(availables)

if __name__ == "__main__":
    main()
