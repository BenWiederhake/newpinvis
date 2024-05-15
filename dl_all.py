#!/usr/bin/env python3

import datetime
import hashlib
import json
import os
import random
import requests
import time


DOWNLOAD_USERAGENT = "pin_crawl ()"
DOWNLOAD_URL = "https://api.pwnedpasswords.com/range/{hash_prefix}"
DOWNLOAD_FILENAME = "target/{hash_prefix}.range"
SKIP_EXISTING = True


def make_hash_table():
    table = dict()
    for pin in range(10000):
        pin_str = f"{pin:04}"
        assert len(pin_str) == 4, (pin, pin_str)
        table[pin_str] = hashlib.sha1(pin_str.encode()).hexdigest().upper()
    return table


def download_prefix(prefix):
    # Prevent catastrophically wrong usage:
    assert len(prefix) == 5 and prefix.isalnum()
    filename = DOWNLOAD_FILENAME.format(hash_prefix=prefix)
    if SKIP_EXISTING and os.path.exists(filename):
        print(f"File {filename} already exists; skipping!")
        return
    time.sleep(0.1)  # Make sure we do not flood their service too badly.
    with open(filename, "w") as fp:
        r = requests.get(
            DOWNLOAD_URL.format(hash_prefix=prefix),
            headers={"user-agent": DOWNLOAD_USERAGENT},
        )
        assert r.status_code == 200, (prefix, r)
        # Note: Yes, 'iter_content' might be more efficient for very large responses,
        # but I expect <100 KiB per response, so there should not be a terrible difference.
        fp.write(r.text)


def report_progress(dt_start, completed_downloads, len_prefixes):
    dt_now = datetime.datetime.now()
    dt_eta = dt_start + (dt_now - dt_start) * len_prefixes / completed_downloads
    print(f"Finished {completed_downloads:5} of {len_prefixes} downloads; ETA is {dt_eta}")


def download_all(prefixes):
    dt_start = datetime.datetime.now()
    print(f"Started download at {dt_start}")
    for i, prefix in enumerate(prefixes):
        download_prefix(prefix)
        if (i + 1) % 1000 == 0:
            completed_downloads = i + 1
            report_progress(dt_start, i + 1, len(prefixes))
    report_progress(dt_start, len(prefixes), len(prefixes))


def run():
    hash_table = make_hash_table()
    with open("target/table.json", "w") as fp:
        json.dump(hash_table, fp)
    prefixes = list(set(hashhex[:5] for hashhex in hash_table.values()))
    # Shuffling is mostly pointless, but sliiiightly obfuscates what we're doing.
    random.shuffle(prefixes)
    download_all(prefixes)


if __name__ == "__main__":
    run()
