#!/usr/bin/env python3

from PIL import Image
import json
import math


# As of writing, max_count is around 2.6 million, the smallest amount is 0, and the second-smallest
# amount is 516. That's probably the reason why 6754 and 7571 don't show up at all: They *were*
# present originally, but presumably less often than 500 times, and someone filtered it out.
MIN_POSITIVE_COUNT = 400
ZOOM_FACTOR = 10


def color_for(count, max_count):
    frac = 1 - math.log10(max(MIN_POSITIVE_COUNT, count) / max_count) / math.log10(MIN_POSITIVE_COUNT / max_count)
    assert 0.0 <= frac <= 1.0, (count, max_count, frac)
    if frac < 1 / 3:
        r = frac * 3
        g = 0.0
        b = 0.0
    elif frac < 2 / 3:
        r = 1.0
        g = frac * 3 - 1
        b = 0.4
    else:
        r = 1.0
        g = 1.0
        b = 0.4 + 0.5 * (frac * 3 - 2)
    r = max(0, min(int(round(r * 255)), 255))
    g = max(0, min(int(round(g * 255)), 255))
    b = max(0, min(int(round(b * 255)), 255))
    return (r, g, b)


def make_img(pin_count_list):
    assert len(pin_count_list) == 10000
    max_count = max(pin_count_list)
    print(f"{max_count=}")
    data = [None for _ in range(10000 * ZOOM_FACTOR * ZOOM_FACTOR)]
    for lhs in range(100):
        for rhs in range(100):
            pin = lhs * 100 + rhs
            pin_count = pin_count_list[pin]
            x = rhs
            y = 99 - lhs
            rgb = color_for(pin_count, max_count)
            for dy in range(ZOOM_FACTOR):
                for dx in range(ZOOM_FACTOR):
                    eff_x = ZOOM_FACTOR * x + dx
                    eff_y = ZOOM_FACTOR * y + dy
                    data[eff_x + (100 * ZOOM_FACTOR) * eff_y] = rgb
    img = Image.new("RGB", (100 * ZOOM_FACTOR, 100 * ZOOM_FACTOR))
    img.putdata(data)
    return img


def run():
    with open("target/list.json", "r") as fp:
        pin_count_list = json.load(fp)
    img = make_img(pin_count_list)
    img.save("target/plot.png")


if __name__ == "__main__":
    run()
