#!/usr/bin/env python3.8

# Standard library imports:
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, FileType
from itertools import chain
from operator import itemgetter

# Third-party imports:
from boltons.iterutils import unique
from pandas import DataFrame, read_csv

def parse_args():
    # Construct the argument parser.
    parser = ArgumentParser(
        "Calculate Experience",
        description="Totals experience by player.",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("data", type=FileType(), help="Input CSV.")
    parser.add_argument("--all", help="Keyword indicated global experience.")
    parser.set_defaults(**{
        "all": "All",
    })
    return parser.parse_args()

if __name__ == "__main__":
    # Parse the arguments.
    args = parse_args()

    # Read the input CSV as row-based dictionaries.
    data = read_csv(args.data).to_dict(orient="records")

    # Convert each comma-delimited value to a list.
    for row in data:
        row["Characters"] = list(map(str.strip, row["Characters"].split(",")))

    # Compute the global set of characters.
    characters = set(chain(*map(itemgetter("Characters"), data)))

    # Ignore character name used as the keyword indicator.
    characters -= {args.all}

    # Update each character keyword in the records.
    for row in data:
        if row["Characters"] == [args.all]:
            row["Characters"] = list(characters)

    # Construct the set of totals per character.
    totals = dict.fromkeys(characters, 0)

    # Compute the running totals.
    for row in data:
        print(row)
        for character in row["Characters"]:
            totals[character] += row["Total"]

    # Convert the totals to a data frame and output it.
    output = DataFrame.from_records(
        list(totals.items()),
        columns=["Character", "Total"]
    ).set_index("Character")
    print(output)
