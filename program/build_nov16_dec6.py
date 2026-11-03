#!/usr/bin/env python3
"""Open gym, both TVs, Nov 16 - Dec 6, 2026 (written 2026-11-03).

Build (TV 1) enters the STRENGTH block (conjugate, triphasic 2/2/2, French contrast heavy step = ME lift):
  wk 7 Ecc 1 (Nov 16): 3 reps, 6-sec lower @ RPE 7   (~76%, tempo-adjusted)
  wk 8 Ecc 2 (Nov 23): 3 reps, 5-sec lower @ RPE 7.5 (~78%)
  wk 9 Iso 1 (Nov 30): 3 reps, 3-sec pause @ RPE 8   (~82%)
  Accessories cut back in the eccentric weeks (rule 7). Bench (Tue) runs the same tempo wave as 4 straight sets.
Athlete (TV 2) finishes its strength block:
  Iso 2 (Nov 16): 3 reps, 3-sec pause @ RPE 8.5 (~84%, tempo-adjusted)
  Conc 1 (Nov 23): 3 fast reps @ RPE 8 (~86%, RTS chart)
  Conc 2 (Nov 30): 2 fast reps @ RPE 8.5-9 (~91%)
  Power block starts Dec 7 (written by the weekly routine).

Same rack layout and helpers as build_oct19_nov15.py.
Run: python3 program/build_nov16_dec6.py
"""
import json, datetime as dt, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_oct19_nov15 import J, fc, WARM, SUNDAY, emom, amrap, fortime, intervals, finish, ROOT  # noqa: E402

START = dt.date(2026, 11, 16)
THANKSGIVING = dt.date(2026, 11, 26)

# ───────────────────────── BUILD (TV 1): Strength wk 7-9 ─────────────────────────
B_HEAVY = {
    7: ("3 · 6-sec lower @ RPE 7", "Eccentric wk 1: 6 sec down, then drive up hard"),
    8: ("3 · 5-sec lower @ RPE 7.5", "Eccentric wk 2: heavier, 5 sec down"),
    9: ("3 · 3-sec pause @ RPE 8", "Isometric wk 1: dead-stop 3-sec pause at the bottom, no bounce"),
}
B_BLOCK = {7: "Strength · Eccentric · Week 1 of 6", 8: "Strength · Eccentric · Week 2 of 6", 9: "Strength · Isometric · Week 3 of 6"}
B_NOTE = {
    7: "Strength block starts. The heavy step of every French contrast is today's main lift: 6 seconds down, then explode. Expect soreness, so accessories are cut back.",
    8: "Eccentric wk 2: more weight on the bar, 5-second lowering. Write down your heavy-step weight.",
    9: "Isometric phase: 3-second dead-stop pause at the bottom of every main-lift rep. Heavier than last week.",
}

def build_week(w):
    heavy, tnote = B_HEAVY[w]
    v = w - 7
    pick = lambda *a: a[v]
    fcn = f"{tnote} · 10–20 sec between steps, 3:00 between rounds · every jump max intent"
    days = [
        {"title": "Lower ME: Squat", "warmup": WARM["squat"],
         "jumps": [fc(4, f"Back Squat {heavy}", "Box Jump 5", "DB Jump Squat 5", "Pogo Hops 10", fcn, 20),
                   J("Pogo Hops", pick("2 × 20", "2 × 25", "3 × 20"), "Quick off the floor, stiff ankles", pick(40, 50, 60))]
                  + ([J("Vertical Jump", pick("", "3 × 4", "3 × 5"), "Max height, land soft", pick(0, 12, 15))] if v else []),
         "strength": [["DB Reverse Lunge", pick("3 × 8/leg @ RPE 7.5", "3 × 8/leg @ RPE 8", "3 × 6/leg · 2-sec pause @ RPE 8"), "Rest 1:30"],
                      ["Loaded Hip Airplane", pick("2 × 5/side", "3 × 5/side", "3 × 6/side"), "Slow, hold a rack or wall"],
                      ["Copenhagen Plank", pick("2 × 25 sec/side", "3 × 25 sec/side", "3 × 30 sec/side"), "Short lever (knee) to scale"]],
         "cond": pick(emom(10, "5 rounds · strength block: quality over speed", ["Min 1: 12 KB Goblet Squats", "Min 2: 10/7 cal Assault bike"], "Bike taken? 100m run"),
                      emom(12, "6 rounds", ["Min 1: 12 KB Goblet Squats", "Min 2: 12/9 cal Assault bike"], "Bike taken? 150m run"),
                      emom(12, "4 rounds", ["Min 1: 12 KB Goblet Squats", "Min 2: 12/9 cal Assault bike", "Min 3: 50 yd Farmer's Carry"], "Bike taken? 150m run")),
         "note": B_NOTE[w]},
        {"title": "Upper ME: Bench", "warmup": WARM["push"],
         "jumps": [J("Pogo Hops", pick("3 × 25", "3 × 30", "3 × 30"), "Quick off the floor", pick(75, 90, 90)),
                   J("Ankle Spring Series", pick("2 × 10", "2 × 10", "3 × 10"), "Stiff ankles, fast feet", pick(20, 20, 30)),
                   J("Plyometric Push-Up", pick("4 × 4", "4 × 5", "5 × 5"), "Hands leave the floor · knees to scale")],
         "strength": [["Bench Press", f"4 × {heavy}", f"{tnote} · rest 3:00"],
                      ["Seated DB Shoulder Press", pick("3 × 8 @ RPE 7.5", "3 × 8 @ RPE 8", "3 × 6 · 2-sec pause @ RPE 8"), "Rest 1:30"],
                      ["Elevated Bird Dog Row", pick("3 × 8/side", "3 × 10/side", "4 × 8/side, heavier"), "Flat back, pull to the hip"],
                      ["DB Tricep Extension + Face Pull", pick("2 × 10 + 15", "3 × 10 + 15", "3 × 8 + 15, heavier"), "Superset, rest 1:00"]],
         "cond": pick(amrap(10, "Steady pace, good reps", ["8 DB Push Press", "12 KB Swings", "200m run (treadmill or outside)"], "Lighter bells · run → 15 cal bike"),
                      amrap(12, "Steady pace, good reps", ["10 DB Push Press", "12 KB Swings", "200m run (treadmill or outside)"], "Lighter bells · run → 15 cal bike"),
                      amrap(12, "Beat last week's rounds", ["10 DB Push Press", "15 KB Swings", "200m run (treadmill or outside)"], "Lighter bells · run → 15 cal bike")),
         "note": B_NOTE[w]},
        {"title": "Lower ME: Hinge", "warmup": WARM["hinge"],
         "jumps": [fc(4, f"Trap Bar Deadlift {heavy}", "Broad Jump 4", "DB Jump Squat 5", "Pogo Hops 10", fcn, 19),
                   J("Lateral Bounds", pick("3 × 5/side", "3 × 6/side", "3 × 6/side"), "Stick each landing 1 sec", pick(30, 36, 36)),
                   J("Pogo Hops", pick("2 × 15", "2 × 20", "2 × 20"), "Quick off the floor", pick(30, 40, 40))]
                  + ([J("Box Drop to Stick", "2 × 5", "Drop, stick, freeze 2 sec", 10)] if v == 2 else []),
         "strength": [["Single-Leg RDL", pick("3 × 8/side @ RPE 7.5", "3 × 8/side @ RPE 8", "3 × 6/side · 2-sec pause @ RPE 8"), "Hold a rack if you need balance"],
                      ["Nordic Hamstring Curl", pick("3 × 4", "3 × 5", "3 × 5, slower"), "Slow lowering · band assist OK"],
                      ["Calf Raises / Cool Guy Leans", pick("3 × 15", "3 × 15, heavier", "3 × 12 · 3-sec hold at the top"), "Pause at the top"]],
         "cond": pick(intervals(6, 60, 90, "Hard 1:00, easy 1:30", ["Treadmill Sprint or Assault bike", "Sled Push, alternate partners"], "Machines taken? Run outside, same times"),
                      intervals(7, 60, 90, "Hard 1:00, easy 1:30", ["Treadmill Sprint or Assault bike", "Sled Push, alternate partners"], "Machines taken? Run outside, same times"),
                      intervals(8, 60, 90, "Hard 1:00, easy 1:30", ["Treadmill Sprint or Assault bike", "Sled Push, alternate partners"], "Machines taken? Run outside, same times")),
         "note": B_NOTE[w]},
        {"title": "Lower ME: Front Squat + Pull", "warmup": WARM["fsq"],
         "jumps": [fc(4, f"Front Squat {heavy}", "Hurdle Hops 5", "DB Jump Squat 5", "Pogo Hops 10", fcn + " · elbows high · no hurdles? Tuck jumps", 20),
                   J("Lateral Pogo Hops", pick("2 × 20", "2 × 25", "3 × 20"), "Side to side over a line", pick(40, 50, 60))],
         "strength": [["Pull-Up", pick("4 × 3 · 5-sec lower", "5 × 3 · 5-sec lower", "5 × 3 · 3-sec hold chin over bar"), "Band or Banded Lat Pulldown to scale · rest 2:00"],
                      ["Cable Row with Extension", pick("3 × 8/side", "3 × 10/side", "4 × 8/side, heavier"), "Cable taken? Dumbbell Rows"],
                      ["Zottman Curl", pick("2 × 10", "3 × 10", "3 × 8, heavier"), "Slow on the way down"]],
         "cond": pick(fortime("15-12-9 for time", 10, "Cap 10 min", ["KB Swings", "Medicine Ball Slams"], "Lighter bell · ball"),
                      fortime("21-15-9 for time", 12, "Cap 12 min", ["KB Swings", "Medicine Ball Slams", "Cal Assault bike (or 2× the reps as walking lunge steps)"], "Lighter bell · ball"),
                      fortime("21-15-9 for time", 12, "Beat last week's time", ["KB Swings", "Medicine Ball Slams", "Cal Assault bike (or 2× the reps as walking lunge steps)"], "Lighter bell · ball")),
         "note": B_NOTE[w]},
        {"title": "Full Body + French Contrast", "warmup": WARM["full"],
         "jumps": [fc(4, "Goblet Squat 3 (heavy, RPE 8)", "Lateral Bounds 3/side", "DB Jump Squat 5", "Pogo Hops 10", "Rest 10–20 sec between steps, 3:00 between rounds", 21),
                   J("Ankle Spring Series", pick("2 × 20", "2 × 25", "3 × 20"), "Stiff ankles, fast feet", pick(40, 50, 60))],
         "strength": [["Rear Foot Elevated Split Squat", pick("4 × 5/side · 6-sec lower @ RPE 7", "4 × 5/side · 5-sec lower @ RPE 7.5", "4 × 5/side · 3-sec pause @ RPE 8"), "Rest 1:30 · same tempo as the week's main lifts"],
                      ["Dumbbell Rows", pick("3 × 8/side", "4 × 8/side", "4 × 8/side, heavier"), "Pause at the hip"],
                      ["Single-Arm Farmer Walk", pick("3 × 40 yd/side", "3 × 50 yd/side", "4 × 50 yd/side"), "Stand tall, don't lean"],
                      ["TK Palof", pick("3 × 10/side", "3 × 12/side", "3 × 12/side, heavier band"), "Ribs down"]],
         "cond": pick(amrap(10, "Max rounds", ["6 DB Push Press", "8 Medicine Ball Slams", "10 KB Goblet Squats"], "Lighter DBs"),
                      amrap(10, "Heavier DBs than last week", ["8 DB Push Press", "8 Medicine Ball Slams", "10 KB Goblet Squats"], "Lighter DBs"),
                      amrap(12, "Max rounds", ["8 DB Push Press", "10 Medicine Ball Slams", "10 KB Goblet Squats", "5 Pull-Ups"], "Band pull-ups or Dumbbell Rows")),
         "note": B_NOTE[w]},
        {"title": "Saturday Partner WOD", "warmup": WARM["sat"],
         "jumps": [J("Pogo Hops", "4 × 20", "Partner counts", 80),
                   J("Broad Jump", pick("4 × 5", "5 × 5", "6 × 5"), "Stick every landing", pick(20, 25, 30))],
         "strength": [["Farmer's Carry", pick("4 × 50 yd, heavy", "4 × 60 yd, heavy", "5 × 60 yd, heavier"), "One partner carries, one rests"],
                      ["Kettlebell Teapot", pick("3 × 8/side", "3 × 10/side", "3 × 10/side, heavier"), "Slow and controlled"]],
         "cond": pick(amrap(18, "Partners split reps any way", ["20 KB Swings", "200m run together", "20 Walking Lunge steps", "10 Pull-Ups"], "Band pull-ups"),
                      amrap(20, "Partners split reps any way", ["20 KB Swings", "40 yd Sled Push each", "20 Walking Lunge steps", "10 Pull-Ups"], "Sled taken? 200m run"),
                      fortime("Partner for time", 22, "5 rounds · cap 22", ["20 KB Swings", "16 cal Assault bike", "40 yd Farmer's Carry", "10 Inchworm Push-Ups"], "Bike taken? 250m run")),
         "note": B_NOTE[w]},
        dict(SUNDAY),
    ]
    return days

# ───────────────────────── ATHLETE (TV 2): Strength Iso 2 → Conc 2 ─────────────────────────
A_HEAVY = {
    "i2": ("3 · 3-sec pause @ RPE 8.5", "Isometric wk 2: heavier, same dead-stop pause"),
    "c1": ("3 @ RPE 8, fast up", "Concentric wk 1: normal lowering, then drive up as FAST as possible"),
    "c2": ("2 @ RPE 8.5–9, fast up", "Concentric wk 2: heaviest of the block. Every rep max speed"),
}
A_BLOCK = {"i2": "Strength · Isometric · Week 4 of 6", "c1": "Strength · Concentric · Week 5 of 6", "c2": "Strength · Concentric · Week 6 of 6"}
A_NOTE = {
    "i2": "Isometric wk 2: more weight, same 3-second dead stop. Own the bottom.",
    "c1": "Concentric phase: no tempo. Control the way down, then move the bar as fast as you can.",
    "c2": "Last strength week: heaviest doubles of the block, all speed. Power block starts Dec 7.",
}

def ath_week(k):
    heavy, tnote = A_HEAVY[k]
    fcn = f"{tnote} · 10–20 sec between steps, 3:00 between rounds"
    v = {"i2": 0, "c1": 1, "c2": 2}[k]
    pick = lambda *a: a[v]
    return [
        {"title": "Lower ME: Hinge", "warmup": WARM["speed"],
         "jumps": [fc(4, f"Trap Bar Deadlift {heavy}", "Hurdle Hops 5", "DB Jump Squat 5", "Pogo Hops 10", fcn + " · no hurdles? Tuck jumps", 20),
                   J("Lateral Bounds", pick("3 × 6/side", "4 × 5/side", "4 × 5/side"), "Stick each landing 1 sec", pick(36, 40, 40)),
                   J("Single-Leg Hop", pick("3 × 5/side", "3 × 6/side", "3 × 6/side"), "Small hops, stable knee", pick(30, 36, 36))],
         "strength": [["Nordic Hamstring Curl", pick("3 × 5", "3 × 6", "3 × 6, slower"), "Slow lowering · band assist OK"],
                      ["Single-Leg RDL", pick("3 × 8/side · 2-sec pause", "3 × 8/side, heavier", "3 × 6/side, heavier"), "RPE 8"],
                      ["Copenhagen Plank", pick("3 × 30 sec/side", "3 × 35 sec/side", "3 × 35 sec/side"), "Short lever (knee) to scale"]],
         "cond": pick(emom(12, "6 rounds", ["Min 1: 25 yd Sled Push, heavy", "Min 2: 6 Medicine Ball Slams"], "Sled taken? 25-yd shuttle sprint"),
                      emom(12, "6 rounds, heavier sled", ["Min 1: 25 yd Sled Push, heavier", "Min 2: 8 Medicine Ball Slams"], "Sled taken? 25-yd shuttle sprint"),
                      emom(14, "7 rounds", ["Min 1: 25 yd Sled Push, heavier", "Min 2: 8 Medicine Ball Slams"], "Sled taken? 25-yd shuttle sprint")),
         "note": A_NOTE[k]},
        {"title": "Upper ME: Press", "warmup": WARM["upper_ath"],
         "jumps": [J("French Contrast × 4 rounds", f"DB Bench Press {heavy} → Plyometric Push-Up 5 → Med Ball Chest Pass 5 → Medicine Ball Slams 5", fcn),
                   J("Pogo Hops", pick("4 × 25", "4 × 25", "4 × 30"), "Quick off the floor", pick(100, 100, 120)),
                   J("Ankle Spring Series", pick("3 × 10", "3 × 12", "3 × 12"), "Stiff ankles", pick(30, 36, 36))],
         "strength": [["Weighted Pull-Up", pick("4 × 2 · 3-sec hold chin over bar @ RPE 8.5", "5 × 2 @ RPE 8, fast up", "4 × 2 @ RPE 8.5–9, fast up"), "Rest 2:30"],
                      ["Face Pull", "3 × 12", "Pull to the eyes"],
                      ["DB Tricep Extension", pick("3 × 10, heavier", "3 × 8, heavier", "3 × 8, heavier"), "Slow down, fast up"]],
         "cond": pick(amrap(8, "Short and fast", ["8 DB Push Press", "8 Medicine Ball Slams"], "Lighter DBs"),
                      amrap(8, "Heavier DBs than last week", ["8 DB Push Press", "10 Medicine Ball Slams"], "Lighter DBs"),
                      amrap(9, "Beat last week's rounds", ["8 DB Push Press", "10 Medicine Ball Slams"], "Lighter DBs")),
         "note": A_NOTE[k]},
        {"title": "Lower ME: Front Squat + Speed", "warmup": WARM["speed"],
         "jumps": [fc(4, f"Front Squat {heavy}", "Box Jump 5", "DB Jump Squat 5", "Pogo Hops 10", fcn + " · elbows high", 20),
                   J("Single-Leg Bound", pick("3 × 6/side", "4 × 5/side", "4 × 5/side"), "Big and controlled", pick(36, 40, 40)),
                   J("Broad Jump", pick("4 × 5", "5 × 4", "5 × 4"), "Stick every landing", 20)],
         "strength": [["Acceleration Sprint", pick("8 × 30 yd", "6 × 40 yd", "8 × 40 yd"), "Walk back · every rep 100%"],
                      ["Rear Foot Elevated Split Squat", pick("3 × 5/side @ RPE 8.5", "3 × 4/side @ RPE 8.5, fast up", "3 × 4/side @ RPE 9, fast up"), "Rest 1:30"],
                      ["KB Side Plank Corkscrew", "3 × 8/side", "Slow"]],
         "cond": pick(intervals(8, 20, 60, "Max effort · beat last week", ["Treadmill Sprint or 30-yd shuttle"], "Treadmill taken? Shuttle sprint"),
                      intervals(10, 15, 45, "Max effort, short and fast", ["Treadmill Sprint or 20-yd shuttle"], "Treadmill taken? Shuttle sprint"),
                      intervals(10, 20, 60, "Max effort", ["Treadmill Sprint or 30-yd shuttle"], "Treadmill taken? Shuttle sprint")),
         "note": A_NOTE[k]},
        {"title": "Upper DE + Rotation", "warmup": WARM["upper_ath"],
         "jumps": [J("Med Ball Rotational Throw", pick("5 × 5/side", "5 × 6/side", "6 × 5/side"), "Max intent, hips first"),
                   J("Lateral Pogo Hops", pick("3 × 30", "4 × 25", "4 × 25"), "Side to side over a line", pick(90, 100, 100)),
                   J("Vertical Jump", "4 × 5", "Max height, land soft", 20),
                   J("Jump Squats", pick("3 × 5", "3 × 5", "3 × 5"), "Bodyweight, max height", 15)],
         "strength": [["DB Push Press", pick("9 × 3 @ RPE 7", "8 × 2 @ RPE 7.5", "10 × 2 @ RPE 7.5"), "Dynamic effort: moderate DBs moved as FAST as possible · rest 1:00"],
                      ["Dumbbell Rows", pick("4 × 10/side", "4 × 8/side, heavier", "4 × 8/side, heavier"), "Pause at the hip"],
                      ["Palof Rotation", pick("3 × 12/side, 2-sec pause", "3 × 12/side, heavier band", "3 × 12/side, heavier band"), "Ribs down"]],
         "cond": pick(emom(12, "6 rounds, heavier bell", ["Min 1: 10 Medicine Ball Slams", "Min 2: 12 KB Swings"], "Lighter ball"),
                      emom(12, "6 rounds", ["Min 1: 10 Medicine Ball Slams", "Min 2: 15 KB Swings"], "Lighter ball"),
                      emom(14, "7 rounds", ["Min 1: 10 Medicine Ball Slams", "Min 2: 15 KB Swings"], "Lighter ball")),
         "note": A_NOTE[k]},
        {"title": "Lower ME: Back Squat", "warmup": WARM["speed"],
         "jumps": [fc(4, f"Back Squat {heavy}", "Hurdle Hops 5", "Trap Bar Jump 5", "Pogo Hops 10", fcn + " · no hurdles? Tuck jumps", 20),
                   J("Lateral Bounds", pick("4 × 5/side", "4 × 6/side", "4 × 6/side"), "Stick each landing 1 sec", pick(40, 48, 48)),
                   J("Single-Leg Hop", pick("3 × 6/side", "3 × 6/side", "3 × 6/side"), "Small hops, stable knee", 36),
                   J("Box Drop to Stick", "3 × 5", "Drop, stick, freeze 2 sec", 15)],
         "strength": [["Loaded Hip Airplane", pick("3 × 6/side, heavier", "3 × 6/side, heavier", "3 × 6/side, heavier"), "Slow, hold a rack or wall"],
                      ["Pissing Dog", pick("3 × 12/side", "3 × 15/side", "3 × 15/side"), "Slow"],
                      ["Calf Raises / Cool Guy Leans", pick("4 × 15", "4 × 15, heavier", "4 × 12, heavier"), "Pause at the top"]],
         "cond": pick(intervals(8, 20, 60, "All-out 20 sec", ["Assault bike or Treadmill Sprint"], "Machines taken? 40-yd sprint"),
                      intervals(10, 15, 45, "All-out 15 sec", ["Assault bike or Treadmill Sprint"], "Machines taken? 30-yd sprint"),
                      intervals(10, 20, 60, "All-out 20 sec", ["Assault bike or Treadmill Sprint"], "Machines taken? 40-yd sprint")),
         "note": A_NOTE[k]},
        {"title": "Saturday Sprint Day", "warmup": WARM["speed"],
         "jumps": [J("Pogo Hops", "3 × 20", "Quick off the floor", 60),
                   J("Broad Jump", pick("5 × 4", "5 × 5", "5 × 5"), "Stick every landing", pick(20, 25, 25)),
                   J("Accel Sprint + Repeated Broad Jump", pick("7 × (1 + 3)", "8 × (1 + 3)", "8 × (1 + 3)"), "Sprint 10 yd into 3 broad jumps", pick(21, 24, 24))],
         "strength": [["Sprint", pick("8 × 40 yd", "10 × 40 yd", "6 × 60 yd"), "Full recovery · every rep 100%"],
                      ["Sled Push", pick("5 × 30 yd", "6 × 30 yd", "6 × 30 yd, heavier"), "Heavy, low hips"]],
         "cond": pick(emom(16, "Partners alternate minutes", ["10 KB Swings", "8 Medicine Ball Slams"], "Lighter bell"),
                      emom(16, "Partners alternate minutes, heavier bell", ["10 KB Swings", "8 Medicine Ball Slams"], "Lighter bell"),
                      emom(18, "Partners alternate minutes", ["10 KB Swings", "8 Medicine Ball Slams"], "Lighter bell")),
         "note": A_NOTE[k]},
        dict(SUNDAY),
    ]

def main():
    report = []
    written = {"wods": [], "wods/t2": []}
    for i, (w, k) in enumerate([(7, "i2"), (8, "c1"), (9, "c2")]):
        monday = START + dt.timedelta(weeks=i)
        for folder, days, block in [("wods", build_week(w), B_BLOCK[w]), ("wods/t2", ath_week(k), A_BLOCK[k])]:
            per_day = []
            for d, day in enumerate(days):
                date = monday + dt.timedelta(days=d)
                if date == THANKSGIVING:
                    day = dict(day, note="Happy Thanksgiving. Get your training in early, then go eat. " + day["note"])
                out, c = finish(day, date, block)
                (ROOT / folder / f"{date.isoformat()}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
                written[folder].append(date.isoformat())
                per_day.append(c)
            report.append((folder, monday.isoformat(), block, per_day))
    for folder, dates in written.items():
        idx = ROOT / folder / "index.json"
        cur = json.loads(idx.read_text())
        idx.write_text(json.dumps(sorted(set(cur) | set(dates)), indent=2) + "\n")
    for folder, mon, block, pd in report:
        flag = " ⚠️ day under 80" if min(pd[:6]) < 80 else ""
        print(f"{'Build  ' if folder == 'wods' else 'Athlete'} {mon} {block:38s} contacts M-Sat {pd[:6]} = {sum(pd[:6])}{flag}")

if __name__ == "__main__":
    main()
