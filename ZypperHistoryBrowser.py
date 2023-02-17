#!/usr/bin/env python

# Author: Ron Shabi

import argparse
from datetime import datetime

DEFAULT_FILE_LOCATION = "/var/log/zypp/history"
DISCARDED = ["#", "zypper", "yast"]

parser = argparse.ArgumentParser(
    description="Browse package manager Zypper's history"
)
parser.add_argument(
    "--actions",
    required=False,
    nargs="+",
    choices=[
        "install",
        "remove",
        "verify",
        "source-install",
        "update",
        "patch",
        "info",
        "refresh",
        "clean",
    ],
    help="Filter by action",
)
parser.add_argument(
    "--from",
    dest="arg_from",
    required=False,
    type=str,
    help="Filter from date (inclusive)",
)
parser.add_argument(
    "--to",
    dest="arg_to",
    required=False,
    type=str,
    help="Filter until date (inclusive)",
)

def parse_optional_date_string(date_string, incase_empty):
    if date_string is None:
        return incase_empty
    else:
        try:
            ret = datetime.fromisoformat(date_string)
            return ret
        except ValueError:
            print(f"Date {date_string} is not a valid IsoFormat date")
            exit(1)


def print_entries(entries):
    for entry in entries:
        print(f"{entry[0].strftime('%Y-%m-%d %H:%M')}\t{entry[1]}\t\t{entry[2]} ({entry[3]})")

if __name__ == "__main__":
    args = parser.parse_args()
    actions = args.actions
    date_from = parse_optional_date_string(args.arg_from, datetime.min)
    date_to = parse_optional_date_string(args.arg_to, datetime.max)

    try:
        entries = []

        with open(DEFAULT_FILE_LOCATION) as f:
            lines = f.readlines()

            # eat lines with discarded chars
            lines = [line for line in lines if not any(c in line for c in DISCARDED)]

            # eat lines with discarded words
            lines = [
                line
                for line in lines
                if not any(word.lower() in DISCARDED for word in line)
            ]

            for line in lines:
                elems = line.split("|")

                entry_date = datetime.fromisoformat(elems[0])
                entry_action = elems[1]
                entry_package = elems[2]
                entry_version = elems[3]

                # Filter by date range
                if (
                    entry_date >= date_from
                    and entry_date <= date_to
                ):

                    # Filter by actions
                    if (
                        actions is None
                        or actions is not None
                        and entry_action in actions
                    ):
                        entry = [entry_date, entry_action, entry_package, entry_version]
                        entries.append(entry)

    except PermissionError:
        print(f"Insufficient privileges to access zypper history file ({DEFAULT_FILE_LOCATION}). Are you root?")

    finally:
        print_entries(entries)