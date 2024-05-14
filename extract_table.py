#!/usr/bin/env python3

import json
import sys

RANGE_FILENAME = "target/{hash_prefix}.range"



def lookup_count(hashhex, real_pin):
    prefix = hashhex[:5]
    suffix = hashhex[5:]
    assert prefix + suffix == hashhex
    filename = RANGE_FILENAME.format(hash_prefix=prefix)
    try:
        with open(filename) as fp:
            for line in fp:
                if not line:
                    continue  # Empty line or last line
                parts = line.rstrip("\n").split(":")
                assert len(parts) == 2
                if parts[0] == suffix:
                    return int(parts[1])
    except FileNotFoundError as e:
        print(f"WARNING: {filename} missing?! Assuming count 0!", file=sys.stderr)
        return 0
    print(f"WARNING: No entry for {real_pin} ({hashhex=})?! Assuming count 0, but that's implausible!", file=sys.stderr)
    # Apparently 6754 and 7571 used to be very secure (until now, sorry for ruining it).
    return 0


def run():
    with open("target/table.json", "r") as fp:
        hash_table = json.load(fp)
    pin_counts = {pin: lookup_count(hashhex, pin) for pin, hashhex in hash_table.items()}
    assert len(pin_counts) == 10000
    pin_count_list = []
    for pin in range(10000):
        pin_str = f"{pin:04}"
        assert len(pin_str) == 4, (pin, pin_str)
        pin_count_list.append(pin_counts[pin_str])
    with open("target/list.json", "w") as fp:
        json.dump(pin_count_list, fp, separators=",:")


if __name__ == "__main__":
    run()
