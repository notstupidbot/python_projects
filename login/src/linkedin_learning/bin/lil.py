#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))
from login import login
import argparse

def build(args):
    print(f"Build: {args.input}")

def watch(args):
    print(f"Watch: {args.input}")

def serve(args):
    print("Serve")

def clean(args):
    print("Clean")

def main():
    parser = argparse.ArgumentParser(description="lil linkedin learning fetcher cli")
    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

    # Build subcommand
    login_parser = subparsers.add_parser("login", help="Login to linkedin learning to create cookies")

    # Watch subcommand
    fetch_parser = subparsers.add_parser("fetch", help="Fetch course metadata")
    fetch_parser.add_argument("url", help="Course url")

     # Watch subcommand
    download_parser = subparsers.add_parser("download", help="Download course items")
    download_parser.add_argument("course", help="Download Course")

    course_parser = subparsers.add_parser("course", help="List saved course")

    account_parser = subparsers.add_parser("account", help="Check for a valid tickets")
    # Serve subcommand
    args = parser.parse_args()

    if args.subcommand == "login":
        login()
    elif args.subcommand == "fetch":
        print(args)
    elif args.subcommand == "course":
        print(args)
    elif args.subcommand == "clean":
        clean(args)
    else:
        print("Error: Invalid subcommand. Use --help for usage.")

if __name__ == "__main__":
    main()
