# Hinge Auto-Liker (MuMu emulator)

Automatically taps the like heart and **Send Like** on Hinge running in the MuMu emulator.

Normal action recorders replay taps at fixed x,y positions, which fails because Hinge's
heart moves with each photo or prompt. This script takes a screenshot, finds the heart and the
Send Like button **by how they look** (OpenCV template matching), and taps wherever they are.

> **Disclaimer:** Hinge's terms prohibit automation, and emulator-plus-bot behavior is exactly what
> their detection looks for. Your account can be shadowbanned or banned. Use at your own risk and
> never with an account you can't afford to lose. This script likes the first photo or prompt it
> sees on each profile without reading the profile. This project is not affiliated with Hinge.

## How it works

1. Screenshot the emulator over ADB (`uiautomator2`).
2. Look for `heart_small.png` in the screenshot (ignoring the bottom menu bar). If it isn't visible, scroll and retry.
3. Tap the heart, then look for `send_like.png`. If it isn't visible, scroll and retry up to 3 times.
4. Tap Send Like, wait a random 3 to 6 seconds, repeat until `MAX_LIKES`.

It stops by itself if it can't find the heart 5 times in a row, or can't find Send Like (a popup, or you hit the daily limit).

## Requirements

- Windows, [MuMu Player 12](https://www.mumuplayer.com/) with Hinge installed and logged in
- Python 3.10+ (tick **"Add Python to PATH"** when installing)
- ADB debugging enabled in MuMu's settings

## Setup (one time)

**1. Install dependencies**
```
pip install -r requirements.txt
```

**2. Find MuMu's `adb.exe`**
```
where /r "C:\Program Files\Netease" adb.exe
```
Use the folder from the `...\nx_device\12.0\shell\adb.exe` result and put it in `ADB_DIR` at the top of `start.bat`.

**3. Check the connection** (MuMu running and fully booted)
```
set PATH=%PATH%;<your ADB folder>
adb connect 127.0.0.1:16384
adb devices
```
You should see `127.0.0.1:16384    device`. Older MuMu versions use port `7555`. If you change the port, update it in `start.bat`, `like_loop.py` and `make_template.py`.

**4. Capture the screen with Hinge open** on a profile where the black heart is visible and the comment box is closed:
```
python make_template.py shot
```
Open `screen.png` in Paint and note the pixel coordinates (hover to read them in the status bar).

**5. Create the two template images**
```
python make_template.py crop heart_small X1 Y1 X2 Y2
python make_template.py crop send_like X1 Y1 X2 Y2
```
- `heart_small`: a tight crop of the **inside** of the black circle with the white heart. Leave out the white card around it, or it won't match hearts that sit on photos.
- `send_like`: the pale pink "Send Like" button. Tap a heart manually first so the button is on screen, then run `shot` again.

Open both PNGs to check they contain only what they should. These are resolution-specific. Templates made on a 1080x1920 emulator won't match a different size, so make them on the same emulator window size you'll run on.

## Running

1. Open MuMu and wait for it to load.
2. In Hinge, tap the **H** icon (bottom left) for the main feed and scroll to a profile with a heart visible and the comment box closed.
3. Double-click `start.bat`.

Press **Ctrl+C** in the window to stop. Edit `MAX_LIKES` in `like_loop.py` to change how many likes it sends. Start with 2.

## Troubleshooting

| Problem | Fix |
|---|---|
| `adb is not recognized` | `ADB_DIR` in `start.bat` is wrong, re-run step 2 |
| Nothing connects | Make sure MuMu is fully booted and ADB debugging is on. Try port `7555` |
| Taps the bottom menu or the wrong screen | Return to the main feed (H icon). Remake `heart_small.png` so it contains only the inside of the circle |
| `Missing template image` | Create `heart_small.png` and `send_like.png` (step 5) |
| Heart score is always low | Re-crop the template tighter, or capture it on the same emulator size you're running |
| `Could not find Send Like` | A popup is covering the screen, or you've hit the daily like limit |

## Privacy

`screen.png` is overwritten on every screenshot and holds whatever Hinge last showed, which is a real person's photo.
It stays on your machine, and `.gitignore` keeps it out of git. **Don't commit screenshots, and don't use real profiles in README images.**
