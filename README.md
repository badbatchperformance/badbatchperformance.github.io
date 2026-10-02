# Bad Batch WOD Board

Workout of the Day for the gym TVs and members' phones. It's a plain static site hosted free on GitHub Pages.

## Links (after GitHub Pages is on)
| Where | URL |
|---|---|
| **TV 1: Build track** (strength + metcon) | `<site>/?wall=both&track=1` |
| **TV 2: Athlete track** (power, speed, jumps) | `<site>/?wall=both&track=2` |
| Split one track over two TVs (optional) | `<site>/?wall=a&track=1` and `<site>/?wall=b&track=1` |
| Phones / social link (track tabs) | `<site>/` |
| Any day | `<site>/?date=2026-10-05` |

## How it updates
- One file per day per track. Build: `wods/YYYY-MM-DD.json`. Athlete: `wods/t2/YYYY-MM-DD.json`. Each folder has an `index.json` listing its posted dates.
- If a column has too much text for the screen, it shrinks itself to fit.
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
