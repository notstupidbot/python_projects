#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))
from login import login
from course import course
from fetch import fetch
from download import download
import argparse



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
    download_parser.add_argument("-i","--id", help="Course id")

    
    course_parser = subparsers.add_parser("course", help="List saved course")
    course_parser.add_argument("-i","--id", help="Course id")

    # account_parser = subparsers.add_parser("account", help="Check for a valid tickets")
    # Serve subcommand
    args = parser.parse_args()

    if args.subcommand == "login":
        login()
    elif args.subcommand == "fetch":
        fetch(args)
    elif args.subcommand == "course":
        course(args)
    elif args.subcommand == "download":
        download(args)
    else:
        print("Error: Invalid subcommand. Use --help for usage.")

if __name__ == "__main__":
    main()
