#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
import re


def read_lammps_log(filename):
    """
    Extract thermo tables from a LAMMPS log file.
    """

    tables = []

    with open(filename, "r") as f:
        lines = f.readlines()

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        # Look for thermo header
        if line.startswith("Step"):

            header = line.split()

            data = []

            i += 1

            while i < len(lines):

                row = lines[i].strip()

                # stop at non-numeric lines
                if not row:
                    break

                if row.startswith(("Loop", "ERROR", "WARNING")):
                    break

                values = row.split()

                if len(values) != len(header):
                    break

                try:
                    values = [float(x) for x in values]
                    data.append(values)
                except ValueError:
                    break

                i += 1

            if data:
                df = pd.DataFrame(data, columns=header)

                tables.append(df)

        i += 1

    if not tables:
        raise RuntimeError("No thermo data found in log file")

    # Combine multiple runs
    df = pd.concat(tables, ignore_index=True)

    return df


def plot_timeseries(df):
    if "Step" not in df.columns:
        raise RuntimeError("No Step column found")

    for column in df.columns:
        if column == "Step":
            continue

        filename = f"{column}.png"

        plt.figure(figsize=(7, 4))
        plt.plot(df["Step"], df[column], linewidth=1)

        plt.xlabel("Step")
        plt.ylabel(column)
        plt.title(f"{column} vs Step")
        plt.grid(True, which="both")
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()

        print("Saved:", filename)


def main():
    parser = argparse.ArgumentParser(
        description="Plot all thermo quantities from LAMMPS log file"
    )

    parser.add_argument("logfile", help="LAMMPS log file")
    parser.add_argument(
        "-s",
        "--min-step",
        type=int,
        default=None,
        help="Ignore data points with Step < MIN_STEP",
    )

    args = parser.parse_args()

    print("Reading log...")
    df = read_lammps_log(args.logfile)

    print("\nDetected quantities:")
    for col in df.columns:
        print(" ", col)

    if args.min_step is not None:
        n_before = len(df)
        df = df[df["Step"] >= args.min_step].reset_index(drop=True)
        print(f"Skipped {n_before - len(df)} data points with Step < {args.min_step}")

    if df.empty:
        raise RuntimeError("No data left after applying --min-step filter")

    plot_timeseries(df)


if __name__ == "__main__":
    main()
