# Bad Batch WOD Board

Workout of the Day for the gym TVs and members' phones. It's a plain static site hosted free on GitHub Pages.

## Links (after GitHub Pages is on)
| Where | URL |
|---|---|
| Wall 1 TV (warm-up, jumps, strength) | `<site>/?wall=a` |
| Wall 2 TV (conditioning + timer) | `<site>/?wall=b` |
| One TV, everything | `<site>/?wall=both` |
| Phones / social link | `<site>/` |
| Any day | `<site>/?date=2026-10-05` |

## How it updates
- One file per day: `wods/YYYY-MM-DD.json`. `wods/index.json` lists every posted date.
- The page loads today's file (by the TV's clock), checks for edits every 5 minutes and switches at midnight.
- `config.json` holds the sign-up link, spots left, prices, hours and the rotating ticker lines.
- Claude writes each week of workouts and pushes them here. Wes reviews at `<site>/?date=...`.

## TV setup (each wall)
1. Plug in the Fire TV Stick and connect to gym Wi-Fi.
2. Install the **Silk Browser** app (Amazon Appstore, free).
3. Open the wall's URL above and add it as a bookmark.
4. Go full screen: Silk menu → "Full screen" (or press the ☰ menu button).
5. **Turn off the screensaver:** Settings → Display & Sounds → Screensaver → Start Time → Never.
6. In the TV's own settings, turn off auto power-off / eco sleep.

Timer on Wall 2: **OK** = start / pause, **◀** = reset. There's a 10-second "get ready" countdown with beeps (turn the TV volume up).
