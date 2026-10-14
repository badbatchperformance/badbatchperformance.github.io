#!/usr/bin/env python3
"""Open gym, both TVs, Oct 19 - Nov 15, 2026 (written 2026-10-14).

Rebuilt to Wes's programming standard (2026-10-10):
  1. Progressive overload every week, never an identical week (Build: hypertrophy wave with a wk-4 unload;
     Athlete: power wk 3 = heavy single, then triphasic 2/2/2 in the strength block).
  2. Back squat AND front squat every week, by day. Single-leg work is the accessory.
  3. Trap bar is the main hinge.
  4. French contrast opens every lower day.
  5. RPE on every heavy lift (open gym has no coach on the floor, so RPE leads).
  6. Sessions ~60 min.

Rack layout (one track on the racks per day):
  Mon Build Back Squat (racks)  / Athlete Trap Bar FC
  Tue Build Bench (racks)       / Athlete DB Bench FC
  Wed Build Trap Bar FC         / Athlete Front Squat FC (racks)
  Thu Build Front Squat (racks) / Athlete DB Push Press + rotation
  Fri Build goblet FC + RFESS   / Athlete Back Squat FC (racks)

Run: python3 program/build_oct19_nov15.py   (writes wods/*.json, wods/t2/*.json, updates both index.json)
"""
import json, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = dt.date(2026, 10, 19)

# Each jump item: (name, dose, note, contacts). contacts=0 for throws / non-contact work.
def J(name, dose, note, contacts=0):
    return {"row": [name, dose, note], "c": contacts}

def fc(rounds, heavy, plyo, loaded, fast, note, per_round):
    return J(f"French Contrast × {rounds} rounds", f"{heavy} → {plyo} → {loaded} → {fast}", note, rounds * per_round)

WARM = {
    "squat": "Foam roll 2 min, then 2 rounds: Goblet Squat w/ Heartbeat × 8 · Inchworm Push-Up × 6 · CL Dead Bug × 6/side",
    "push": "Foam roll 2 min, then 2 rounds: Lateral Lunge × 6/side · Push-Up to T × 5/side · Bird Dog × 6/side",
    "hinge": "Foam roll 2 min, then 2 rounds: Reverse Lunge × 6/side · Hamstring Walkout × 5 · 4 Way Deadbug × 4",
    "fsq": "Foam roll 2 min, then 2 rounds: KOT Sissy Squat × 8 · Wall Shoulder CAR × 3/side · CL Dead Bug × 6/side",
    "full": "Foam roll 2 min, then 2 rounds: Walking Lunge × 6/side · Inchworm Shoulder Tap × 5 · Bird Dog × 6/side",
    "sat": "Foam roll 2 min, then 2 rounds: Tri-Planar Ankle × 8/side · Inchworm Walk × 4 · CL Dead Bug × 6/side",
    "speed": "Foam roll 2 min, then 2 rounds: Tri-Planar Ankle × 8/side · Inchworm Walk × 4 · CL Dead Bug × 6/side · A-skip 2 × 20 yd · B-skip 2 × 20 yd",
    "upper_ath": "Foam roll 2 min, then 2 rounds: Lateral Lunge × 6/side · Eccentric Push-Up with Extension × 5 · Bird Dog × 6/side",
}

SUNDAY = {
    "title": "Recovery Sunday", "warmup": "Foam roll 5 min", "jumps": [],
    "strength": [["Zone 2 cardio", "30–40 min", "Bike, treadmill walk or outside. 60–70% max heart rate: you can talk in full sentences"]],
    "cond": {"format": "Mobility 10 × 1:00", "subtitle": "5 positions, 2 rounds · 10 sec to switch",
             "timer": {"type": "interval", "work": 60, "rest": 10, "rounds": 10},
             "items": ["Hip Mobility Flow", "Dynamic Pigeon Isometric (each side)", "90/90 with Thoracic Rotation",
                       "Couch Stretch (each side)", "90/90 Breathing: 5 sec in, 5 sec out"],
             "scaling": "Go easy. Nose breathing the whole time"},
    "note": "Recovery is training. Sleep 7–9 hours tonight.",
}

def emom(n, sub, items, scaling): return {"format": f"EMOM {n}", "subtitle": sub, "timer": {"type": "emom", "minutes": n}, "items": items, "scaling": scaling}
def amrap(n, sub, items, scaling): return {"format": f"AMRAP {n}", "subtitle": sub, "timer": {"type": "amrap", "minutes": n}, "items": items, "scaling": scaling}
def fortime(fmt, cap, sub, items, scaling): return {"format": fmt, "subtitle": sub, "timer": {"type": "fortime", "cap": cap}, "items": items, "scaling": scaling}
def intervals(r, w, rest, sub, items, scaling):
    m = lambda s: f"{s // 60}:{s % 60:02d}" if s >= 60 else f":{s:02d}"
    return {"format": f"{r} × {m(w)} / {m(rest)}", "subtitle": sub, "timer": {"type": "interval", "work": w, "rest": rest, "rounds": r}, "items": items, "scaling": scaling}

# ───────────────────────── BUILD (TV 1): Hypertrophy wk 3-6 ─────────────────────────
# Main lifts (Back Squat Mon, Bench Tue, Trap Bar Wed, Front Squat Thu): RPE leads, % is the estimate.
#   wk3 4×6 @7 (~76%) · wk4 UNLOAD 3×8 @6 (~68%) · wk5 4×6 @8 (~79%) · wk6 3×5 @8 (~81%; fewer sets so FC singles + work sets stay ≤20 reps in the 80-90% zone)
MAIN = {3: "4 × 6 @ RPE 7", 4: "3 × 8 @ RPE 6", 5: "4 × 6 @ RPE 8", 6: "3 × 5 @ RPE 8"}
MAIN_NOTE = {3: "Rest 2:30 · new scheme: heavier, 6s", 4: "Rest 2:00 · UNLOAD week: lighter on purpose, crisp reps",
             5: "Rest 2:30 · heavier than wk 3", 6: "Rest 3:00 · heaviest week of the block"}
FC_ROUNDS = {3: 2, 4: 2, 5: 3, 6: 3}
FC_HEAVY = {3: "2 @ RPE 7", 4: "2 @ RPE 6", 5: "2 @ RPE 7.5", 6: "1 @ RPE 7"}
ACC = {3: "3 × 10", 4: "2 × 10", 5: "3 × 12", 6: "4 × 10"}          # hypertrophy accessories
ACC_RPE = {3: "@ RPE 8", 4: "@ RPE 7", 5: "@ RPE 8", 6: "@ RPE 8.5"}
CORE_S = {3: "3 × 25 sec", 4: "2 × 20 sec", 5: "3 × 30 sec", 6: "3 × 35 sec"}
WEEK_NOTE = {
    3: "New this week: trap bar is the Wednesday hinge, front squat is Thursday, and French contrast opens every lower day.",
    4: "UNLOAD week. Everything is lighter on purpose so you come back stronger. Don't add weight.",
    5: "Back to work: heavier than week 3. Same lifts, more on the bar.",
    6: "Heaviest week of the block. Strength block starts Nov 16.",
}

def build_week(w):
    r, h = FC_ROUNDS[w], FC_HEAVY[w]
    days = []
    # Mon: Back Squat
    days.append({
        "title": "Lower: Squat", "warmup": WARM["squat"],
        "jumps": [
            fc(r, f"Back Squat {h}", "Box Jump 5", "DB Jump Squat 5", "Pogo Hops 10", "Rest 10–20 sec between steps, 3:00 between rounds · every jump max intent", 20),
            J("Pogo Hops", {3: "3 × 20", 4: "2 × 20", 5: "3 × 20", 6: "3 × 25"}[w], "Quick off the floor, stiff ankles", {3: 60, 4: 40, 5: 60, 6: 75}[w]),
        ] + ([J("Vertical Jump", {3: "3 × 4", 5: "3 × 4", 6: "4 × 4"}[w], "Max height, land soft", {3: 12, 5: 12, 6: 16}[w])] if w != 4 else []),
        "strength": [
            ["Back Squat", MAIN[w], MAIN_NOTE[w]],
            ["DB Reverse Lunge", f"{ACC[w]}/leg {ACC_RPE[w]}", "Rest 1:30"],
            ["Loaded Hip Airplane", {3: "3 × 5/side", 4: "2 × 5/side", 5: "3 × 6/side", 6: "3 × 6/side, heavier"}[w], "Slow, hold a rack or wall"],
            ["Copenhagen Plank", f"{CORE_S[w]}/side", "Short lever (knee) to scale"],
        ],
        "cond": {
            3: emom(12, "3 rounds · new station every minute", ["Min 1: 12 KB Goblet Squats", "Min 2: 10/7 cal Assault bike", "Min 3: 20 Walking Lunge steps", "Min 4: 40 yd Farmer's Carry"], "Bike taken? 100m run · lighter bells"),
            4: emom(8, "2 rounds · easy pace, unload week", ["Min 1: 10 KB Goblet Squats", "Min 2: 8/6 cal Assault bike", "Min 3: 16 Walking Lunge steps", "Min 4: 40 yd Farmer's Carry"], "Bike taken? 100m run"),
            5: emom(16, "4 rounds · new station every minute", ["Min 1: 12 KB Goblet Squats", "Min 2: 12/9 cal Assault bike", "Min 3: 20 Walking Lunge steps", "Min 4: 40 yd Farmer's Carry"], "Bike taken? 150m run · lighter bells"),
            6: emom(16, "4 rounds · heavier bells than wk 5", ["Min 1: 15 KB Goblet Squats", "Min 2: 12/9 cal Assault bike", "Min 3: 24 Walking Lunge steps", "Min 4: 50 yd Farmer's Carry"], "Bike taken? 150m run · lighter bells"),
        }[w],
        "note": WEEK_NOTE[w],
    })
    # Tue: Bench
    days.append({
        "title": "Upper: Push", "warmup": WARM["push"],
        "jumps": [
            J("Pogo Hops", {3: "3 × 30", 4: "3 × 20", 5: "3 × 30", 6: "3 × 35"}[w], "Quick off the floor", {3: 90, 4: 60, 5: 90, 6: 105}[w]),
            J("Ankle Spring Series", {3: "2 × 10", 4: "2 × 10", 5: "3 × 10", 6: "3 × 10"}[w], "Stiff ankles, fast feet", {3: 20, 4: 20, 5: 30, 6: 30}[w]),
            J("Plyometric Push-Up", {3: "4 × 5", 4: "3 × 4", 5: "4 × 5", 6: "5 × 5"}[w], "Hands leave the floor · knees to scale"),
        ],
        "strength": [
            ["Bench Press", MAIN[w], MAIN_NOTE[w]],
            ["Seated DB Shoulder Press", f"{ {3: '3 × 10', 4: '2 × 10', 5: '3 × 12', 6: '4 × 10'}[w] } {ACC_RPE[w]}".replace("  ", " "), "Rest 1:30"],
            ["Elevated Bird Dog Row", f"{ACC[w]}/side", "Flat back, pull to the hip"],
            ["DB Tricep Extension + Face Pull", f"{ {3: '3', 4: '2', 5: '3', 6: '4'}[w] } × 12 + 15", "Superset, rest 1:00"],
        ],
        "cond": {
            3: amrap(12, "Steady pace, good reps", ["10 DB Push Press", "12 KB Swings", "200m run (treadmill or outside)"], "Lighter bells · run → 15 cal bike"),
            4: amrap(8, "Unload: easy pace", ["8 DB Push Press", "10 KB Swings", "200m run (treadmill or outside)"], "Lighter bells"),
            5: amrap(14, "Steady pace, good reps", ["10 DB Push Press", "15 KB Swings", "200m run (treadmill or outside)"], "Lighter bells · run → 15 cal bike"),
            6: amrap(15, "Beat your wk 5 rounds", ["12 DB Push Press", "15 KB Swings", "250m run (treadmill or outside)"], "Lighter bells · run → 18 cal bike"),
        }[w],
        "note": WEEK_NOTE[w],
    })
    # Wed: Trap Bar
    days.append({
        "title": "Lower: Hinge", "warmup": WARM["hinge"],
        "jumps": [
            fc(r, f"Trap Bar Deadlift {h}", "Broad Jump 4", "DB Jump Squat 5", "Pogo Hops 10", "Rest 10–20 sec between steps, 3:00 between rounds · every jump max intent", 19),
            J("Lateral Bounds", {3: "3 × 6/side", 4: "2 × 5/side", 5: "3 × 6/side", 6: "3 × 6/side"}[w], "Stick each landing 1 sec", {3: 36, 4: 20, 5: 36, 6: 36}[w]),
            J("Pogo Hops", {3: "2 × 20", 4: "2 × 15", 5: "2 × 20", 6: "2 × 25"}[w], "Quick off the floor", {3: 40, 4: 30, 5: 40, 6: 50}[w]),
        ] + ([J("Box Drop to Stick", "2 × 5", "Drop, stick, freeze 2 sec", 10)] if w == 6 else []),
        "strength": [
            ["Trap Bar Deadlift", MAIN[w], MAIN_NOTE[w] + " · trap bar keeps load off the spine"],
            ["Single-Leg RDL", f"{ACC[w]}/side {ACC_RPE[w]}", "Hold a rack if you need balance"],
            ["Nordic Hamstring Curl", {3: "3 × 4", 4: "2 × 4", 5: "3 × 5", 6: "3 × 6"}[w], "Slow lowering · band assist OK"],
            ["Calf Raises / Cool Guy Leans", {3: "3 × 15", 4: "2 × 15", 5: "3 × 15", 6: "3 × 20"}[w], "Pause at the top"],
        ],
        "cond": {
            3: intervals(6, 60, 90, "Hard 1:00, easy 1:30", ["Treadmill Sprint or Assault bike", "Sled Push, alternate partners"], "Machines taken? Run outside, same times"),
            4: intervals(4, 60, 120, "Unload: moderate effort", ["Assault bike or run", "Steady, not all-out"], "Machines taken? Run outside"),
            5: intervals(8, 60, 90, "Hard 1:00, easy 1:30", ["Treadmill Sprint or Assault bike", "Sled Push, alternate partners"], "Machines taken? Run outside, same times"),
            6: intervals(8, 60, 60, "Hard 1:00, easy 1:00 · less rest than wk 5", ["Treadmill Sprint or Assault bike", "Sled Push, alternate partners"], "Machines taken? Run outside, same times"),
        }[w],
        "note": WEEK_NOTE[w],
    })
    # Thu: Front Squat + Pull
    days.append({
        "title": "Lower: Front Squat + Pull", "warmup": WARM["fsq"],
        "jumps": [
            fc(r, f"Front Squat {h}", "Hurdle Hops 5", "DB Jump Squat 5", "Pogo Hops 10", "Rest 10–20 sec between steps, 3:00 between rounds · no hurdles? Tuck jumps", 20),
            J("Lateral Pogo Hops", {3: "3 × 20", 4: "2 × 20", 5: "3 × 20", 6: "3 × 25"}[w], "Side to side over a line", {3: 60, 4: 40, 5: 60, 6: 75}[w]),
        ],
        "strength": [
            ["Front Squat", MAIN[w], MAIN_NOTE[w] + " · elbows high"],
            ["Pull-Up", {3: "5 × (2 short of failure)", 4: "3 × (3 short of failure)", 5: "5 × (1 short of failure)", 6: "6 × (1 short of failure)"}[w], "Band or Banded Lat Pulldown to scale"],
            ["Cable Row with Extension", f"{ACC[w]}/side", "Cable taken? Dumbbell Rows"],
            ["Zottman Curl", {3: "3 × 12", 4: "2 × 12", 5: "3 × 12, heavier", 6: "4 × 10, heavier"}[w], "Slow on the way down"],
        ],
        "cond": {
            3: fortime("21-15-9 for time", 12, "Cap 12 min", ["KB Swings", "Medicine Ball Slams", "Cal Assault bike (or 2× the reps as walking lunge steps)"], "Lighter bell · ball"),
            4: fortime("15-12-9 for time", 8, "Unload: smooth, not all-out", ["KB Swings", "Medicine Ball Slams"], "Lighter bell · ball"),
            5: fortime("21-15-9 for time", 12, "Beat your wk 3 time", ["KB Swings", "Medicine Ball Slams", "Cal Assault bike (or 2× the reps as walking lunge steps)"], "Lighter bell · ball"),
            6: fortime("27-21-15 for time", 15, "Cap 15 min", ["KB Swings", "Medicine Ball Slams", "Cal Assault bike (or 2× the reps as walking lunge steps)"], "Lighter bell · ball"),
        }[w],
        "note": WEEK_NOTE[w],
    })
    # Fri: Full body, rack-free
    fr = {3: 3, 4: 2, 5: 3, 6: 4}[w]
    days.append({
        "title": "Full Body + French Contrast", "warmup": WARM["full"],
        "jumps": [
            fc(fr, "Goblet Squat 3 (heavy, RPE 8)", "Lateral Bounds 3/side", "DB Jump Squat 5", "Pogo Hops 10", "Rest 10–20 sec between steps, 3:00 between rounds", 21),
            J("Ankle Spring Series", {3: "2 × 25", 4: "2 × 20", 5: "3 × 20", 6: "2 × 25"}[w], "Stiff ankles, fast feet", {3: 50, 4: 40, 5: 60, 6: 50}[w]),
        ],
        "strength": [
            ["Rear Foot Elevated Split Squat", {3: "4 × 8/side @ RPE 8", 4: "3 × 8/side @ RPE 7", 5: "4 × 10/side @ RPE 8", 6: "4 × 8/side @ RPE 8.5"}[w], "Rest 1:30 · heavier DBs than last time you did 8s"],
            ["Dumbbell Rows", {3: "4 × 10/side", 4: "3 × 10/side", 5: "4 × 12/side", 6: "5 × 10/side"}[w], "Pause at the hip"],
            ["Single-Arm Farmer Walk", {3: "3 × 40 yd/side", 4: "2 × 40 yd/side", 5: "3 × 50 yd/side", 6: "4 × 50 yd/side"}[w], "Stand tall, don't lean"],
            ["TK Palof", {3: "3 × 10/side", 4: "2 × 10/side", 5: "3 × 12/side", 6: "3 × 12/side, heavier band"}[w], "Ribs down"],
        ],
        "cond": {
            3: amrap(10, "Max rounds", ["6 DB Push Press", "8 Medicine Ball Slams", "10 KB Goblet Squats"], "Lighter DBs"),
            4: amrap(8, "Unload: steady", ["6 DB Push Press", "8 Medicine Ball Slams", "8 KB Goblet Squats"], "Lighter DBs"),
            5: amrap(12, "Max rounds", ["8 DB Push Press", "10 Medicine Ball Slams", "12 KB Goblet Squats"], "Lighter DBs"),
            6: amrap(12, "Beat wk 5", ["10 DB Push Press", "10 Medicine Ball Slams", "12 KB Goblet Squats", "6 Pull-Ups"], "Band pull-ups or Dumbbell Rows"),
        }[w],
        "note": WEEK_NOTE[w],
    })
    # Sat: Partner
    days.append({
        "title": "Saturday Partner WOD", "warmup": WARM["sat"],
        "jumps": [
            J("Pogo Hops", {3: "4 × 20", 4: "3 × 20", 5: "4 × 20", 6: "4 × 20"}[w], "Partner counts", {3: 80, 4: 60, 5: 80, 6: 80}[w]),
            J("Broad Jump", {3: "5 × 5", 4: "4 × 5", 5: "5 × 5", 6: "6 × 5"}[w], "Stick every landing", {3: 25, 4: 20, 5: 25, 6: 30}[w]),
        ],
        "strength": [
            ["Farmer's Carry", {3: "4 × 60 yd", 4: "3 × 50 yd", 5: "4 × 60 yd, heavier", 6: "5 × 60 yd, heavier"}[w], "One partner carries, one rests"],
            ["Kettlebell Teapot", {3: "3 × 8/side", 4: "2 × 8/side", 5: "3 × 10/side", 6: "3 × 10/side, heavier"}[w], "Slow and controlled"],
        ],
        "cond": {
            3: amrap(20, "Partners split reps any way", ["20 KB Swings", "200m run together", "20 Walking Lunge steps", "10 Pull-Ups"], "Band pull-ups"),
            4: amrap(14, "Unload: conversational pace", ["16 KB Swings", "200m run together", "16 Walking Lunge steps"], "Lighter bells"),
            5: amrap(22, "Partners split reps any way", ["20 KB Swings", "40 yd Sled Push each", "20 Walking Lunge steps", "10 Pull-Ups"], "Sled taken? 200m run"),
            6: fortime("Partner for time", 25, "5 rounds · cap 25", ["20 KB Swings", "20 cal Assault bike", "40 yd Farmer's Carry", "10 Inchworm Push-Ups"], "Bike taken? 300m run"),
        }[w],
        "note": WEEK_NOTE[w],
    })
    days.append(dict(SUNDAY))
    return days

# ───────────────────────── ATHLETE (TV 2) ─────────────────────────
# Power wk 3 (Oct 19): approved wave 80-82×3 → 85-87×2 → 90×1 with volume down ~60%. Heavy step = single @ RPE 7.5 (~90%).
# Strength block (Oct 26+): conjugate with triphasic 2/2/2 on the main lifts; French contrast is the DE slot.
#   Ecc wk1 (Oct 26): 3 reps, 6-sec lower @ RPE 7   Ecc wk2 (Nov 2): 3 reps, 5-sec lower @ RPE 8   Iso wk1 (Nov 9): 3 reps, 3-sec pause @ RPE 8
TEMPO = {
    "e1": ("3 · 6-sec lower @ RPE 7", "Eccentric wk 1: 6 sec down, then drive up hard"),
    "e2": ("3 · 5-sec lower @ RPE 8", "Eccentric wk 2: heavier, 5 sec down"),
    "i1": ("3 · 3-sec pause @ RPE 8", "Isometric wk 1: dead-stop 3-sec pause at the bottom, no bounce"),
}
ATH_BLOCK = {"p3": "Power · Week 3 of 3", "e1": "Strength · Eccentric · Week 1 of 6", "e2": "Strength · Eccentric · Week 2 of 6", "i1": "Strength · Isometric · Week 3 of 6"}
ATH_NOTE = {
    "p3": "Last power week: heaviest single of the block, much less volume. Every rep fast.",
    "e1": "Strength block starts. Slow 6-second lowering on the main lift, then explode. Expect soreness: accessories are cut back.",
    "e2": "Eccentric wk 2: heavier than last week, 5-second lowering.",
    "i1": "Isometric phase: 3-second dead-stop pause at the bottom of every main-lift rep. Heavier again.",
}

def ath_power_wk3():
    fcn = "Rest 10–20 sec between steps, 3:00 between rounds · heavy single, then fast"
    return [
        {"title": "Lower Power: Hinge", "warmup": WARM["speed"],
         "jumps": [fc(4, "Trap Bar Deadlift 1 @ RPE 7.5 (~90%)", "Hurdle Hops 4", "Trap Bar Jump 4", "Pogo Hops 8", fcn + " · no hurdles? Tuck jumps", 16),
                   J("Lateral Bounds", "2 × 5/side", "Stick each landing 1 sec", 20)],
         "strength": [["Nordic Hamstring Curl", "2 × 5", "Slow lowering · band assist OK"],
                      ["Loaded Hip Airplane", "2 × 5/side", "Slow, hold a rack or wall"],
                      ["Copenhagen Plank", "2 × 25 sec/side", "Short lever (knee) to scale"]],
         "cond": emom(8, "4 rounds · max intent", ["Min 1: 20 yd Sled Push, heavy", "Min 2: 5 Medicine Ball Slams"], "Sled taken? 20-yd shuttle sprint"),
         "note": ATH_NOTE["p3"]},
        {"title": "Upper Power: Press", "warmup": WARM["upper_ath"],
         "jumps": [J("French Contrast × 4 rounds", "DB Bench Press 2 (heavy, RPE 8) → Plyometric Push-Up 4 → Med Ball Chest Pass 4 → Medicine Ball Slams 4", "Rest 10–20 sec between steps, 3:00 between rounds"),
                   J("Pogo Hops", "3 × 25", "Quick off the floor", 75), J("Ankle Spring Series", "1 × 10", "Stiff ankles", 10)],
         "strength": [["Weighted Pull-Up", "4 × 2 @ RPE 8.5", "Heavier than wk 2 · rest 2:30"],
                      ["MB Pitcher Throw", "3 × 4/side", "Max intent"],
                      ["Face Pull", "2 × 15", "Pull to the eyes"]],
         "cond": amrap(6, "Short and fast", ["6 DB Push Press", "8 Medicine Ball Slams"], "Lighter DBs"),
         "note": ATH_NOTE["p3"]},
        {"title": "Speed + Hinge Power", "warmup": WARM["speed"],
         "jumps": [J("Pogo Hops", "2 × 20", "Quick off the floor", 40), J("Broad Jump", "4 × 3", "Stick every landing", 12),
                   J("Single-Leg Bound", "2 × 5/side", "Big and controlled", 20), J("Box Drop to Stick", "2 × 4", "Drop, stick, freeze 2 sec", 8)],
         "strength": [["Acceleration Sprint", "5 × 30 yd", "Full recovery, walk back · every rep 100%"],
                      ["Heavy KB Swings", "4 × 6", "Snap the hips · heaviest bell you can move fast"]],
         "cond": intervals(5, 10, 50, "Short sprints, full rest", ["Treadmill Sprint or 20-yd shuttle"], "Treadmill taken? Shuttle sprint"),
         "note": ATH_NOTE["p3"]},
        {"title": "Upper Speed + Rotation", "warmup": WARM["upper_ath"],
         "jumps": [J("Windmill MB Throw", "3 × 5/side", "Max intent, full rotation"), J("Lateral Pogo Hops", "3 × 20", "Side to side over a line", 60),
                   J("Vertical Jump", "3 × 4", "Max height, land soft", 12), J("Jump Squats", "2 × 5", "Bodyweight, max height", 10)],
         "strength": [["DB Push Press", "5 × 2 @ RPE 8", "Racks are Build's today · drive the DBs fast"],
                      ["Cable Row with Extension", "2 × 10/side", "Cable taken? Dumbbell Rows"],
                      ["Palof Rotation", "2 × 10/side", "Ribs down"]],
         "cond": emom(8, "4 rounds", ["Min 1: 8 Medicine Ball Slams", "Min 2: 10 KB Swings"], "Lighter ball"),
         "note": ATH_NOTE["p3"]},
        {"title": "Lower Power: Squat", "warmup": WARM["speed"],
         "jumps": [fc(4, "Back Squat 1 @ RPE 7.5 (~90%)", "Box Jump 4", "DB Jump Squat 4", "Pogo Hops 8", fcn, 16),
                   J("Hurdle Hops", "3 × 5", "No hurdles? Tuck jumps", 15), J("Single-Leg Bound", "2 × 4/side", "Big and controlled", 16)],
         "strength": [["Rear Foot Elevated Split Squat", "2 × 6/side @ RPE 7", "Rest 1:30"],
                      ["Pissing Dog", "2 × 10/side", "Slow"],
                      ["Calf Raises / Cool Guy Leans", "3 × 12", "Pause at the top"]],
         "cond": intervals(5, 20, 70, "All-out 20 sec", ["Assault bike or Treadmill Sprint"], "Machines taken? 40-yd sprint"),
         "note": ATH_NOTE["p3"]},
        {"title": "Saturday Sprint Day", "warmup": WARM["speed"],
         "jumps": [J("Pogo Hops", "3 × 20", "Quick off the floor", 60), J("Broad Jump", "3 × 4", "Stick every landing", 12),
                   J("Accel Sprint + Repeated Broad Jump", "5 × (1 + 3)", "Sprint 10 yd into 3 broad jumps", 15)],
         "strength": [["Sprint", "6 × 40 yd", "Full recovery · every rep 100%"], ["Sled Push", "4 × 25 yd", "Heavy, low hips"]],
         "cond": emom(10, "Partners alternate minutes", ["8 KB Swings", "6 Medicine Ball Slams"], "Lighter bell"),
         "note": ATH_NOTE["p3"]},
        dict(SUNDAY),
    ]

def ath_strength(k):
    heavy, tnote = TEMPO[k]
    fcn = f"{tnote} · 10–20 sec between steps, 3:00 between rounds"
    v = {"e1": 0, "e2": 1, "i1": 2}[k]
    pick = lambda *a: a[v]
    return [
        {"title": "Lower ME: Hinge", "warmup": WARM["speed"],
         "jumps": [fc(4, f"Trap Bar Deadlift {heavy}", "Hurdle Hops 5", "DB Jump Squat 5", "Pogo Hops 10", fcn + " · no hurdles? Tuck jumps", 20),
                   J("Lateral Bounds", pick("3 × 5/side", "3 × 5/side", "3 × 6/side"), "Stick each landing 1 sec", pick(30, 30, 36))]
                  + ([J("Single-Leg Hop", pick("", "3 × 4/side", "3 × 5/side"), "Small hops, stable knee", pick(0, 24, 30))] if v else []),
         "strength": [["Nordic Hamstring Curl", pick("2 × 4", "3 × 4", "3 × 5"), "Slow lowering · band assist OK"],
                      ["Single-Leg RDL", pick("2 × 8/side", "3 × 8/side", "3 × 10/side"), "RPE 7–8"],
                      ["Copenhagen Plank", pick("2 × 20 sec/side", "3 × 25 sec/side", "3 × 30 sec/side"), "Short lever (knee) to scale"]],
         "cond": pick(emom(8, "4 rounds", ["Min 1: 20 yd Sled Push, heavy", "Min 2: 6 Medicine Ball Slams"], "Sled taken? 20-yd shuttle sprint"),
                      emom(10, "5 rounds", ["Min 1: 20 yd Sled Push, heavy", "Min 2: 6 Medicine Ball Slams"], "Sled taken? 20-yd shuttle sprint"),
                      emom(12, "6 rounds", ["Min 1: 25 yd Sled Push, heavy", "Min 2: 6 Medicine Ball Slams"], "Sled taken? 25-yd shuttle sprint")),
         "note": ATH_NOTE[k]},
        {"title": "Upper ME: Press", "warmup": WARM["upper_ath"],
         "jumps": [J("French Contrast × 4 rounds", f"DB Bench Press {heavy} → Plyometric Push-Up 5 → Med Ball Chest Pass 5 → Medicine Ball Slams 5", fcn),
                   J("Pogo Hops", pick("3 × 25", "4 × 25", "4 × 25"), "Quick off the floor", pick(75, 100, 100)),
                   J("Ankle Spring Series", pick("2 × 10", "2 × 10", "3 × 10"), "Stiff ankles", pick(20, 20, 30))],
         "strength": [["Weighted Pull-Up", pick("4 × 4 · 5-sec lower @ RPE 7", "4 × 4 · 5-sec lower @ RPE 8", "4 × 3 · 3-sec hold chin over bar @ RPE 8"), "Rest 2:30"],
                      ["Face Pull", pick("2 × 15", "3 × 15", "3 × 12, heavier"), "Pull to the eyes"],
                      ["DB Tricep Extension", pick("2 × 12", "3 × 12", "3 × 10, heavier"), "Slow down, fast up"]],
         "cond": pick(amrap(6, "Short and fast", ["6 DB Push Press", "8 Medicine Ball Slams"], "Lighter DBs"),
                      amrap(8, "Short and fast", ["6 DB Push Press", "8 Medicine Ball Slams"], "Lighter DBs"),
                      amrap(8, "Heavier DBs than last week", ["8 DB Push Press", "8 Medicine Ball Slams"], "Lighter DBs")),
         "note": ATH_NOTE[k]},
        {"title": "Lower ME: Front Squat + Speed", "warmup": WARM["speed"],
         "jumps": [fc(4, f"Front Squat {heavy}", "Box Jump 5", "DB Jump Squat 5", "Pogo Hops 10", fcn + " · elbows high", 20),
                   J("Single-Leg Bound", pick("3 × 4/side", "3 × 5/side", "3 × 6/side"), "Big and controlled", pick(24, 30, 36))]
                  + ([J("Broad Jump", pick("", "3 × 4", "4 × 4"), "Stick every landing", pick(0, 12, 16))] if v else []),
         "strength": [["Acceleration Sprint", pick("6 × 20 yd", "8 × 20 yd", "6 × 30 yd"), "Walk back · every rep 100%"],
                      ["Rear Foot Elevated Split Squat", pick("2 × 6/side @ RPE 7", "3 × 6/side @ RPE 7.5", "3 × 6/side @ RPE 8"), "Rest 1:30"],
                      ["KB Side Plank Corkscrew", pick("2 × 6/side", "3 × 6/side", "3 × 8/side"), "Slow"]],
         "cond": pick(intervals(6, 15, 45, "Max effort", ["Treadmill Sprint or 20-yd shuttle"], "Treadmill taken? Shuttle sprint"),
                      intervals(8, 15, 45, "Max effort", ["Treadmill Sprint or 20-yd shuttle"], "Treadmill taken? Shuttle sprint"),
                      intervals(8, 20, 60, "Max effort, longer sprint", ["Treadmill Sprint or 30-yd shuttle"], "Treadmill taken? Shuttle sprint")),
         "note": ATH_NOTE[k]},
        {"title": "Upper DE + Rotation", "warmup": WARM["upper_ath"],
         "jumps": [J("Med Ball Rotational Throw", pick("4 × 5/side", "4 × 6/side", "5 × 5/side"), "Max intent, hips first"),
                   J("Lateral Pogo Hops", pick("3 × 20", "3 × 25", "3 × 25"), "Side to side over a line", pick(60, 75, 75)),
                   J("Vertical Jump", "4 × 5", "Max height, land soft", 20)]
                  + ([J("Jump Squats", "2 × 5", "Bodyweight, max height", 10)] if v == 2 else []),
         "strength": [["DB Push Press", pick("6 × 3 @ RPE 7", "7 × 3 @ RPE 7", "8 × 3 @ RPE 7"), "Dynamic effort: moderate DBs moved as FAST as possible · rest 1:00"],
                      ["Dumbbell Rows", pick("3 × 8/side", "3 × 10/side", "4 × 10/side"), "Pause at the hip"],
                      ["Palof Rotation", pick("3 × 10/side", "3 × 12/side", "3 × 12/side, 2-sec pause"), "Ribs down"]],
         "cond": pick(emom(8, "4 rounds", ["Min 1: 8 Medicine Ball Slams", "Min 2: 10 KB Swings"], "Lighter ball"),
                      emom(10, "5 rounds", ["Min 1: 8 Medicine Ball Slams", "Min 2: 10 KB Swings"], "Lighter ball"),
                      emom(10, "5 rounds, heavier bell", ["Min 1: 10 Medicine Ball Slams", "Min 2: 12 KB Swings"], "Lighter ball")),
         "note": ATH_NOTE[k]},
        {"title": "Lower ME: Back Squat", "warmup": WARM["speed"],
         "jumps": [fc(4, f"Back Squat {heavy}", "Hurdle Hops 5", "Trap Bar Jump 5", "Pogo Hops 10", fcn + " · no hurdles? Tuck jumps", 20),
                   J("Lateral Bounds", pick("3 × 5/side", "3 × 6/side", "3 × 6/side"), "Stick each landing 1 sec", pick(30, 36, 36))]
                  + ([J("Single-Leg Hop", pick("", "3 × 4/side", "3 × 5/side"), "Small hops, stable knee", pick(0, 24, 30))] if v else [])
                  + ([J("Box Drop to Stick", "2 × 5", "Drop, stick, freeze 2 sec", 10)] if v == 2 else []),
         "strength": [["Loaded Hip Airplane", pick("2 × 5/side", "3 × 5/side", "3 × 6/side"), "Slow, hold a rack or wall"],
                      ["Pissing Dog", pick("2 × 10/side", "3 × 10/side", "3 × 12/side"), "Slow"],
                      ["Calf Raises / Cool Guy Leans", pick("3 × 12", "3 × 15", "4 × 15"), "Pause at the top"]],
         "cond": pick(intervals(6, 20, 70, "All-out 20 sec", ["Assault bike or Treadmill Sprint"], "Machines taken? 40-yd sprint"),
                      intervals(8, 20, 70, "All-out 20 sec", ["Assault bike or Treadmill Sprint"], "Machines taken? 40-yd sprint"),
                      intervals(8, 20, 60, "All-out 20 sec, less rest", ["Assault bike or Treadmill Sprint"], "Machines taken? 40-yd sprint")),
         "note": ATH_NOTE[k]},
        {"title": "Saturday Sprint Day", "warmup": WARM["speed"],
         "jumps": [J("Pogo Hops", "3 × 20", "Quick off the floor", 60), J("Broad Jump", pick("3 × 4", "4 × 4", "4 × 5"), "Stick every landing", pick(12, 16, 20)),
                   J("Accel Sprint + Repeated Broad Jump", pick("5 × (1 + 3)", "6 × (1 + 3)", "6 × (1 + 3)"), "Sprint 10 yd into 3 broad jumps", pick(15, 18, 18))],
         "strength": [["Sprint", pick("8 × 30 yd", "10 × 30 yd", "8 × 40 yd"), "Full recovery · every rep 100%"],
                      ["Sled Push", pick("6 × 20 yd", "6 × 25 yd", "5 × 30 yd"), "Heavy, low hips"]],
         "cond": pick(emom(12, "Partners alternate minutes", ["8 KB Swings", "6 Medicine Ball Slams"], "Lighter bell"),
                      emom(14, "Partners alternate minutes", ["10 KB Swings", "6 Medicine Ball Slams"], "Lighter bell"),
                      emom(16, "Partners alternate minutes", ["10 KB Swings", "8 Medicine Ball Slams"], "Lighter bell")),
         "note": ATH_NOTE[k]},
        dict(SUNDAY),
    ]

def finish(day, date, block):
    out = {"date": date.isoformat(), "block": block, "title": day["title"], "warmup": day["warmup"],
           "jumps": [j["row"] if isinstance(j, dict) else j for j in day["jumps"]],
           "strength": day["strength"], "cond": day["cond"], "note": day["note"]}
    contacts = sum(j["c"] for j in day["jumps"] if isinstance(j, dict))
    return out, contacts

def main():
    report = []
    weeks_build = [(3, "Hypertrophy · Week 3 of 6"), (4, "Hypertrophy · Week 4 of 6 (unload)"), (5, "Hypertrophy · Week 5 of 6"), (6, "Hypertrophy · Week 6 of 6")]
    weeks_ath = ["p3", "e1", "e2", "i1"]
    written = {"wods": [], "wods/t2": []}
    for i in range(4):
        monday = START + dt.timedelta(weeks=i)
        w, blk = weeks_build[i]
        k = weeks_ath[i]
        for folder, days, block in [("wods", build_week(w), blk), ("wods/t2", ath_power_wk3() if k == "p3" else ath_strength(k), ATH_BLOCK[k])]:
            per_day = []
            for d, day in enumerate(days):
                date = monday + dt.timedelta(days=d)
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
        print(f"{'Build  ' if folder == 'wods' else 'Athlete'} {mon} {block:38s} contacts M-Sat {pd[:6]} = {sum(pd)}")

if __name__ == "__main__":
    main()
