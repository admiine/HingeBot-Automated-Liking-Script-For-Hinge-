"""Hinge auto-liker for the MuMu emulator.

Finds the like heart and the "Send Like" button by image matching (not fixed
coordinates), so it still works when the heart moves around the screen.
"""
import random
import time

import cv2
import uiautomator2 as u2

DEVICE = "127.0.0.1:16384"   # MuMu 12 ADB address (older MuMu: 127.0.0.1:7555)
MAX_LIKES = 2                # raise this once a test run works
THRESHOLD = 0.8              # match confidence needed to tap (0 to 1)
MENU_BAR_FRACTION = 0.9375   # ignore the bottom menu bar (its heart icon looks like the like heart)

d = u2.connect(DEVICE)


def find(template_file):
    """Screenshot the emulator and return (score, x, y) of the best match."""
    d.screenshot("screen.png")
    screen = cv2.imread("screen.png")
    screen = screen[: int(screen.shape[0] * MENU_BAR_FRACTION)]
    template = cv2.imread(template_file)
    if template is None:
        raise SystemExit(f"Missing template image: {template_file} (see README, step 5)")
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, score, _, loc = cv2.minMaxLoc(result)
    h, w = template.shape[:2]
    return score, loc[0] + w // 2, loc[1] + h // 2


def scroll():
    d.swipe(0.5, 0.75, 0.5, 0.35, 0.3)
    time.sleep(random.uniform(1.5, 2.5))


likes = 0
misses = 0

while likes < MAX_LIKES and misses < 5:
    score, x, y = find("heart_small.png")
    print("heart score:", round(score, 2))
    if score <= THRESHOLD:
        misses += 1
        print("heart not visible, scrolling")
        scroll()
        continue

    misses = 0
    d.click(x, y)
    time.sleep(random.uniform(1.5, 2.5))

    sent = False
    for _ in range(3):
        score, x, y = find("send_like.png")
        print("send like score:", round(score, 2))
        if score > THRESHOLD:
            d.click(x, y)
            sent = True
            break
        print("Send Like not visible, scrolling")
        scroll()

    if not sent:
        print("Could not find Send Like, stopping (popup or daily limit?)")
        break

    likes += 1
    print("likes sent:", likes)
    time.sleep(random.uniform(3, 6))

print("done. total likes:", likes)
