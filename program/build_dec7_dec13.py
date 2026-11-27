#!/usr/bin/env python3
"""Open gym, both TVs, Dec 7 - Dec 13, 2026 (written 2026-11-26 by the weekly routine).

Build (TV 1): Strength wk 4 of 6, Isometric wk 2. 4 x 3, 3-sec pause @ RPE 8.5 (~84% tempo-adjusted).
  Max-effort variations rotate this week: Box Squat (Mon), Close-Grip Bench (Tue),
  Deficit Trap Bar Deadlift (Wed). Front Squat stays Thu (back + front squat every week).
Athlete (TV 2): Power wk 1 of 3 (new block). No tempo, heavy step 3 @ RPE 7 (~84%), max bar speed.
Never overwrites an existing date file.
Run: python3 program/build_dec7_dec13.py
"""
import json, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = dt.date(2026, 12, 7)

W_SQUAT = "Foam roll 2 min, then 2 rounds: Goblet Squat w/ Heartbeat × 8 · Inchworm Push-Up × 6 · CL Dead Bug × 6/side"
W_PUSH = "Foam roll 2 min, then 2 rounds: Lateral Lunge × 6/side · Push-Up to T × 5/side · Bird Dog × 6/side"
W_HINGE = "Foam roll 2 min, then 2 rounds: Reverse Lunge × 6/side · Hamstring Walkout × 5 · 4 Way Deadbug × 4"
W_FS = "Foam roll 2 min, then 2 rounds: KOT Sissy Squat × 8 · Wall Shoulder CAR × 3/side · CL Dead Bug × 6/side"
W_FULL = "Foam roll 2 min, then 2 rounds: Walking Lunge × 6/side · Inchworm Shoulder Tap × 5 · Bird Dog × 6/side"
W_SAT = "Foam roll 2 min, then 2 rounds: Tri-Planar Ankle × 8/side · Inchworm Walk × 4 · CL Dead Bug × 6/side"
W_SPEED = W_SAT + " · A-skip 2 × 20 yd · B-skip 2 × 20 yd"
W_UPPER_A = "Foam roll 2 min, then 2 rounds: Lateral Lunge × 6/side · Eccentric Push-Up with Extension × 5 · Bird Dog × 6/side"

SUNDAY = {
    "title": "Recovery Sunday", "warmup": "Foam roll 5 min", "jumps": [],
    "strength": [["Zone 2 cardio", "30–40 min",
                  "Bike, treadmill walk or outside. 60–70% max heart rate: you can talk in full sentences"]],
    "cond": {"format": "Mobility 10 × 1:00", "subtitle": "5 positions, 2 rounds · 10 sec to switch",
             "timer": {"type": "interval", "work": 60, "rest": 10, "rounds": 10},
             "items": ["Hip Mobility Flow", "Dynamic Pigeon Isometric (each side)", "90/90 with Thoracic Rotation",
                       "Couch Stretch (each side)", "90/90 Breathing: 5 sec in, 5 sec out"],
             "scaling": "Go easy. Nose breathing the whole time"},
    "note": "Recovery is training. Sleep 7–9 hours tonight.",
}


def emom(m, sub, items, sc):
    return {"format": f"EMOM {m}", "subtitle": sub, "timer": {"type": "emom", "minutes": m}, "items": items, "scaling": sc}


def amrap(m, sub, items, sc, label=None):
    return {"format": label or f"AMRAP {m}", "subtitle": sub, "timer": {"type": "amrap", "minutes": m}, "items": items, "scaling": sc}


def fortime(cap, label, sub, items, sc):
    return {"format": label, "subtitle": sub, "timer": {"type": "fortime", "cap": cap}, "items": items, "scaling": sc}


def iv(r, w, rest, sub, items, sc):
    f = lambda s: f"{s // 60}:{s % 60:02d}" if s >= 60 else f":{s:02d}"
    return {"format": f"{r} × {f(w)} / {f(rest)}", "subtitle": sub,
            "timer": {"type": "interval", "work": w, "rest": rest, "rounds": r}, "items": items, "scaling": sc}


FC = "French Contrast × 4 rounds"

# ───────────── BUILD: Strength · Week 4 of 6 (Isometric wk 2) ─────────────
BH = "3 · 3-sec pause @ RPE 8.5"
BN = "Isometric wk 2: same 3-sec dead-stop pause, heavier · 10–20 sec between steps, 3:00 between rounds · every jump max intent"
B_NOTE = "Isometric wk 2: same 3-sec pause, more weight. New main-lift variation today: log it."
BUILD = [
    {"title": "Lower ME: Box Squat", "warmup": W_SQUAT,
     "jumps": [[FC, f"Box Squat {BH} → Box Jump 5 → DB Jump Squat 5 → Pogo Hops 12",
                BN + " · parallel box, sit back, stay tight, no rocking"],
               ["Pogo Hops", "3 × 20", "Quick off the floor, stiff ankles"],
               ["Vertical Jump", "4 × 5", "Max height, land soft"]],
     "strength": [["DB Walking Lunge", "3 × 8/leg @ RPE 8", "Rest 1:30"],
                  ["Pissing Dog", "3 × 12/side", "Slow, no hip rotation"],
                  ["KB Side Plank Corkscrew", "3 × 8/side", "Slow"]],
     "cond": amrap(10, "Max rounds", ["10 KB Goblet Squats", "12/9 cal Assault bike", "8 Inchworm Push-Ups"],
                   "Bike taken? 150m run"),
     "note": B_NOTE},
    {"title": "Upper ME: Close-Grip Bench", "warmup": W_PUSH,
     "jumps": [["Pogo Hops", "3 × 30", "Quick off the floor"],
               ["Ankle Spring Series", "3 × 12", "Stiff ankles, fast feet"],
               ["Plyometric Push-Up", "5 × 5", "Hands leave the floor · knees to scale"]],
     "strength": [["Close-Grip Bench Press", f"4 × {BH}",
                   "Hands shoulder-width · dead-stop 3-sec pause on the chest · rest 3:00"],
                  ["Dumbbell Rows", "4 × 8/side", "Pause at the hip"],
                  ["Barbell Skull Crushers + Prone YTW", "3 × 8 + 8", "Superset, rest 1:00"]],
     "cond": emom(12, "4 rounds", ["Min 1: 10 DB Push Press", "Min 2: 15 KB Swings", "Min 3: 12/9 cal Assault bike"],
                  "Bike taken? 150m run · lighter DBs"),
     "note": B_NOTE},
    {"title": "Lower ME: Deficit Hinge", "warmup": W_HINGE,
     "jumps": [[FC, f"Deficit Trap Bar Deadlift {BH} → Broad Jump 4 → DB Jump Squat 5 → Pogo Hops 12",
                BN + " · stand on a 2-in plate, pause just off the floor"],
               ["Lateral Bounds", "3 × 6/side", "Stick each landing 1 sec"],
               ["Pogo Hops", "2 × 20", "Quick off the floor"],
               ["Box Drop to Stick", "2 × 5", "Drop, stick, freeze 2 sec"]],
     "strength": [["Hip Thrust", "3 × 8 · 3-sec hold @ RPE 8", "Back on a plyo box · racks are the Athlete track's"],
                  ["Lengthened Ham Iso", "3 × 30 sec/side", "Long hamstring, push the heel down"],
                  ["Waiter's Walk", "3 × 40 yd/side", "Lock the elbow, ribs down"]],
     "cond": fortime(12, "For time", "4 rounds · cap 12",
                     ["200m run", "15 KB Swings", "10 Medicine Ball Slams"],
                     "Lighter bell · run → 12/9 cal bike"),
     "note": B_NOTE},
    {"title": "Lower ME: Front Squat + Pull", "warmup": W_FS,
     "jumps": [[FC, f"Front Squat {BH} → Hurdle Hops 5 → DB Jump Squat 5 → Pogo Hops 12",
                BN + " · elbows high · no hurdles? Tuck jumps"],
               ["Lateral Pogo Hops", "3 × 20", "Side to side over a line"]],
     "strength": [["Pull-Up", "5 × 3 · 4-sec hold chin over bar", "Band or Banded Lat Pulldown to scale · rest 2:00"],
                  ["Elevated Bird Dog Row", "4 × 8/side", "Flat back, pull to the hip"],
                  ["Face Pull", "3 × 15", "Cable taken? Band face pull"]],
     "cond": iv(6, 40, 80, "Hard :40, easy 1:20",
                ["Assault bike or Treadmill Sprint"], "Machines taken? Shuttle sprints, same times"),
     "note": B_NOTE},
    {"title": "Full Body + French Contrast", "warmup": W_FULL,
     "jumps": [[FC, "Goblet Squat 3 (heavy, RPE 8) → Lateral Bounds 3/side → DB Jump Squat 5 → Pogo Hops 12",
                "Rest 10–20 sec between steps, 3:00 between rounds"],
               ["Ankle Spring Series", "3 × 20", "Stiff ankles, fast feet"]],
     "strength": [["Rear Foot Elevated Split Squat", "4 × 4/side · 3-sec pause @ RPE 8.5",
                   "Rest 1:30 · same tempo as the week's main lifts"],
                  ["HK LM Press to Decel", "3 × 6/side", "Press fast, stop it hard"],
                  ["Cable Row with Extension", "3 × 8/side", "Cable taken? Dumbbell Rows"],
                  ["Palof Rotation", "3 × 10/side", "Ribs down"]],
     "cond": emom(15, "5 rounds", ["Min 1: 10 Medicine Ball Slams", "Min 2: 5 Pull-Ups", "Min 3: 40 yd Farmer's Carry"],
                  "Band pull-ups or Dumbbell Rows"),
     "note": B_NOTE},
    {"title": "Saturday Partner WOD", "warmup": W_SAT,
     "jumps": [["Pogo Hops", "4 × 20", "Partner counts"],
               ["Broad Jump", "7 × 5", "Stick every landing"]],
     "strength": [["Single-Arm Farmer Walk", "4 × 50 yd/side", "One partner carries, one rests"],
                  ["Copenhagen Plank", "3 × 30 sec/side", "Short lever (knee) to scale"]],
     "cond": amrap(20, "Split reps any way", ["20 KB Swings", "15 cal Assault bike", "10 Inchworm Push-Ups",
                                              "40 yd Sled Push"],
                   "Bike taken? 200m run · sled taken? 40-yd shuttle sprint", label="Partner AMRAP 20"),
     "note": "Partner day. Same 3-sec pause on the week's main lifts; today is about moving well together."},
    SUNDAY,
]

# ───────────── ATHLETE: Power · Week 1 of 3 (new block) ─────────────
AH = "3 @ RPE 7, fast"
AN = "Power wk 1: no tempo, lighter bar, every rep max speed · 10–20 sec between steps, 3:00 between rounds"
A_NOTE = "Power block starts: no tempo, lighter heavy step. Move the bar fast, then jump."
ATHLETE = [
    {"title": "Lower Power: Hinge", "warmup": W_SPEED,
     "jumps": [[FC, f"Trap Bar Deadlift {AH} → Broad Jump 4 → Trap Bar Jump 5 → Pogo Hops 10",
                AN + " · trap bar jump 20–30% of your deadlift"],
               ["Single-Leg Bound", "3 × 5/side", "Big and controlled"],
               ["Lateral Bounds", "3 × 6/side", "Stick each landing 1 sec"],
               ["Pogo Hops", "2 × 20", "Quick off the floor"]],
     "strength": [["Nordic Hamstring Curl", "2 × 5", "Slow lowering · band assist OK"],
                  ["Single-Leg RDL", "2 × 6/side", "Hold a rack if you need balance"],
                  ["TK Palof", "2 × 10/side", "Ribs down"]],
     "cond": emom(8, "4 rounds · max intent", ["Min 1: 20 yd Sled Push, heavy", "Min 2: 5 Medicine Ball Slams"],
                  "Sled taken? 20-yd shuttle sprint"),
     "note": A_NOTE},
    {"title": "Upper Power: Press", "warmup": W_UPPER_A,
     "jumps": [[FC, f"DB Bench Press {AH} → Plyometric Push-Up 4 → Med Ball Chest Pass 5 → Medicine Ball Slams 5", AN],
               ["Pogo Hops", "4 × 25", "Quick off the floor"],
               ["Lateral Pogo Hops", "2 × 20", "Side to side over a line"],
               ["Ankle Spring Series", "2 × 10", "Stiff ankles"]],
     "strength": [["Explosive Pull-Up", "5 × 3, fast up", "Bodyweight, chest to bar if you can · band to scale"],
                  ["Elevated Bird Dog Row", "3 × 6/side, fast up", "Pull hard, lower slow"],
                  ["Prone YTW", "2 × 8", "Light, squeeze each position"]],
     "cond": emom(10, "5 rounds · fast reps", ["Min 1: 10 KB Swings", "Min 2: 6 Medicine Ball Slams"], "Lighter bell"),
     "note": A_NOTE},
    {"title": "Speed + Front Squat Power", "warmup": W_SPEED,
     "jumps": [[FC, f"Front Squat {AH} → Box Jump 5 → DB Jump Squat 5 → Pogo Hops 10", AN + " · elbows high"],
               ["Broad Jump", "6 × 4", "Stick every landing"],
               ["Single-Leg Hop", "3 × 5/side", "Small hops, stable knee"],
               ["Box Drop to Stick", "3 × 5", "Drop, stick, freeze 2 sec"]],
     "strength": [["Acceleration Sprint", "8 × 20 yd", "Full recovery, walk back · every rep 100%"],
                  ["Heavy KB Swings", "4 × 6", "Snap the hips · heaviest bell you can move fast"],
                  ["Kettlebell Teapot", "2 × 8/side", "Slow and controlled"]],
     "cond": iv(8, 10, 50, "Short sprints, full rest", ["Treadmill Sprint or 20-yd shuttle"],
                "Treadmill taken? Shuttle sprint"),
     "note": A_NOTE},
    {"title": "Upper Speed + Rotation", "warmup": W_UPPER_A,
     "jumps": [["Windmill MB Throw", "4 × 5/side", "Max intent, full rotation"],
               ["Lateral Pogo Hops", "4 × 25", "Side to side over a line"],
               ["Vertical Jump", "4 × 4", "Max height, land soft"],
               ["Jump Squats", "3 × 5", "Bodyweight, max height"]],
     "strength": [["DB Push Press", "5 × 3 @ RPE 7 + 5 MB Chest Pass",
                   "Contrast: press fast, then throw · racks are Build's today · rest 2:00"],
                  ["Dumbbell Rows", "3 × 6/side, fast up", "Pause at the hip"],
                  ["Copenhagen Plank", "2 × 25 sec/side", "Short lever (knee) to scale"]],
     "cond": amrap(8, "Smooth and fast", ["5 Pull-Ups", "8 Medicine Ball Slams", "10 Walking Lunge steps"],
                   "Band pull-ups or Dumbbell Rows"),
     "note": A_NOTE},
    {"title": "Lower Power: Squat", "warmup": W_SPEED,
     "jumps": [[FC, f"Back Squat {AH} → Hurdle Hops 5 → Trap Bar Jump 5 → Pogo Hops 10",
                AN + " · no hurdles? Tuck jumps"],
               ["Lateral Bounds", "3 × 6/side", "Stick each landing 1 sec"],
               ["Single-Leg Hop", "3 × 5/side", "Small hops, stable knee"]],
     "strength": [["Hip Thrust", "3 × 6, fast up", "Shoulders on the bench, drive hard"],
                  ["Lengthened Ham Iso", "2 × 30 sec/side", "Long hamstring, push the heel down"],
                  ["Calf Raises / Cool Guy Leans", "3 × 10, fast up", "Pause at the top"]],
     "cond": iv(6, 15, 45, "All-out 15 sec", ["Assault bike or Treadmill Sprint"], "Machines taken? 30-yd sprint"),
     "note": A_NOTE},
    {"title": "Saturday Sprint Day", "warmup": W_SPEED,
     "jumps": [["Pogo Hops", "3 × 20", "Quick off the floor"],
               ["Broad Jump", "5 × 4", "Stick every landing"],
               ["Accel Sprint + Repeated Broad Jump", "8 × (1 + 3)", "Sprint 10 yd into 3 broad jumps"],
               ["Hurdle Hops", "3 × 5", "No hurdles? Tuck jumps"]],
     "strength": [["Sprint", "8 × 30 yd", "Full recovery · every rep 100%"],
                  ["Sled Push", "6 × 20 yd, heavy", "Low hips · sled taken? 20-yd sprint"]],
     "cond": amrap(12, "You go, I go", ["A: 2 × 20-yd shuttle sprint", "B: 10 KB Swings", "Switch when A is back"],
                   "Lighter bell · jog the shuttle", label="Partner AMRAP 12"),
     "note": A_NOTE},
    SUNDAY,
]

BUILD_BLOCK = "Strength · Week 4 of 6 (Isometric)"
ATH_BLOCK = "Power · Week 1 of 3"


def write(track_dir, days, block):
    idx_path = track_dir / "index.json"
    idx = json.loads(idx_path.read_text())
    for i, d in enumerate(days):
        date = (START + dt.timedelta(days=i)).isoformat()
        p = track_dir / f"{date}.json"
        if p.exists():
            print("skip (exists)", p)
            continue
        out = {"date": date, "block": block, **d}
        p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
        if date not in idx:
            idx.append(date)
        print("wrote", p)
    idx = sorted(set(idx))
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    write(ROOT / "wods", BUILD, BUILD_BLOCK)
    write(ROOT / "wods" / "t2", ATHLETE, ATH_BLOCK)
