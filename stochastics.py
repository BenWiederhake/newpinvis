#!/usr/bin/env python3

import collections
import json
import math

from plot import MIN_POSITIVE_COUNT


Distrib = collections.namedtuple("Distrib", ["handle", "description", "unscaled_distribution"])


def top_distrib(n, pin_count_list):
    biggest_items = sorted(enumerate(pin_count_list), key=lambda e: e[1])[-n:]
    print(biggest_items)
    unscaled_distribution = [0] * 10000
    for pin, count in biggest_items:
        unscaled_distribution[pin] = count
    return unscaled_distribution


def generate_distribs(pin_count_list):
    distribs = []
    distribs.append(Distrib(
        "real",
        "The actual distribution in the real world, according to HIBP.",
        pin_count_list,
    ))
    distribs.append(Distrib("top1", "Always the most popular PIN.", top_distrib(1, pin_count_list)))
    distribs.append(Distrib("top3", "The three most popular PIN.", top_distrib(3, pin_count_list)))
    distribs.append(Distrib("top10", "The Top-10 of real-life PINs.", top_distrib(10, pin_count_list)))
    distribs.append(Distrib("uni", "Uniformly across *all* possible PINs.", [1] * 10000))
    distribs.append(Distrib(
        "invreal",
        "Inversely probable to the real distribution.",
        [1 / c for c in pin_count_list],
    ))
    # TODO: Uniform across BOTTOM 90%!
    return distribs


def compute_corr(chooser, breaker):
    scale = sum(chooser.unscaled_distribution) * sum(breaker.unscaled_distribution)
    unscaled_corr = sum(pc * pb for pb, pc in zip(chooser.unscaled_distribution, breaker.unscaled_distribution))
    return unscaled_corr / scale


def run():
    with open("target/list.json", "r") as fp:
        pin_count_list = json.load(fp)
    pin_count_list = [max(c, MIN_POSITIVE_COUNT) for c in pin_count_list]
    distribs = generate_distribs(pin_count_list)
    corrs = {d1.handle: {d2.handle: compute_corr(d1, d2) for d2 in distribs} for d1 in distribs}
    probs = {
        # "Reluctant whistle ravioli" is a beacon:
        # https://benwiederhake.github.io/#beacons
        # In short: There are many projects that analyze PIN usage, but this one is mine.
        # The three words reluctant whistle ravioli uniquiely identify *THIS* project.
        "type": "newpinvis_reluctantwhistleravioli_probs_v1",
        "desc": [(d.handle, d.description) for d in distribs],
        "corrs": corrs,
    }
    with open("target/probabilities.json", "w") as fp:
        json.dump(probs, fp)


if __name__ == "__main__":
    run()
