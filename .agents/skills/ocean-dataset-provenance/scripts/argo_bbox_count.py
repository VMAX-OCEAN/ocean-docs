#!/usr/bin/env python3
"""Count Argo profile files in a bbox from the GDAC global index.

Index columns: file,date,latitude,longitude,ocean,profiler_type,institution,date_update
Float id is path segment [1] (dac/float/profiles/file), NOT [2] -- using [2]
collapses every float into one count.

usage: python3 argo_bbox_count.py LAT_MIN LAT_MAX LON_MIN LON_MAX
"""
import csv
import gzip
import io
import sys
import urllib.request

INDEX = "https://data-argo.ifremer.fr/ar_index_global_prof.txt.gz"


def main():
    lat_min, lat_max, lon_min, lon_max = map(float, sys.argv[1:5])
    files = 0
    floats = set()
    dates = []
    with urllib.request.urlopen(INDEX, timeout=300) as resp:
        with gzip.GzipFile(fileobj=resp) as gz:
            text = io.TextIOWrapper(gz, encoding="utf-8", errors="replace")
            for row in csv.reader(text):
                if not row or row[0] == "file" or row[0].startswith("#"):
                    continue
                try:
                    lat, lon = float(row[2]), float(row[3])
                except (IndexError, ValueError):
                    continue
                if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                    files += 1
                    floats.add(row[0].split("/")[1])
                    dates.append(row[1])
    print(f"profile_files={files}")
    print(f"unique_floats={len(floats)}")
    if dates:
        print(f"date_min={min(dates)}")
        print(f"date_max={max(dates)}")
    if len(floats) == 1:
        print("WARNING: one float only -- index layout likely changed; verify the header")


if __name__ == "__main__":
    main()
