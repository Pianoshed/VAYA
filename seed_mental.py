# -*- coding: utf-8 -*-
"""
seed_mental_db.py
-----------------
Run this from the ROOT of your Flask project (same folder as app.py):

    python seed_mental_db.py

It will insert 27 Yoruba-named respondents directly into your
submit-assessment.db SQLite database using the corrected scoring logic.
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Fix Windows console encoding so the script never crashes on special chars
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ── Make sure we can import from the project ──────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Try to use the real Flask app + DB, fall back to direct SQLite ────────────
USE_FLASK = True
try:
    from app import app, db, SubmitAssessment
except Exception as e:
    print(f"[INFO] Could not import Flask app ({e}). Using direct SQLite insert.")
    USE_FLASK = False

if not USE_FLASK:
    import sqlite3
    # Find the DB file — adjust path if yours is different
    DB_CANDIDATES = [
        "instance/submit-assessment.db",
        "submit-assessment.db",
        "instance/default.db",
    ]
    DB_PATH = None
    for p in DB_CANDIDATES:
        if os.path.exists(p):
            DB_PATH = p
            break
    if DB_PATH is None:
        print("[ERROR] Could not find submit-assessment.db. Please set DB_PATH manually.")
        sys.exit(1)
    print(f"[INFO] Using database: {DB_PATH}")

# ── Seed data ─────────────────────────────────────────────────────────────────
random.seed(99)  # fixed seed → same 27 people every run

MALE_FIRST = [
    "Adewale","Babatunde","Damilola","Femi","Gbenga",
    "Idris","Jide","Kayode","Leke","Muyiwa",
    "Niyi","Oluwaseun","Pelumi","Rotimi","Segun",
    "Taiwo","Usman","Kunle","Wole","Tunde",
]
FEMALE_FIRST = [
    "Adaeze","Blessing","Chiamaka","Folake","Grace",
    "Halima","Ifeoma","Jumoke","Kehinde","Latifat",
    "Morenike","Ngozi","Omolara","Ronke","Sade",
    "Titilayo","Uche","Yetunde","Bimpe","Tosin",
]
LAST_NAMES = [
    "Adeyemi","Babatunde","Okonkwo","Adeleke","Okafor",
    "Adesanya","Ogunleye","Balogun","Adeola","Fashola",
    "Oluwole","Afolabi","Gbadamosi","Ojo","Salami",
    "Akintola","Odunsi","Agboola","Ijiwola","Adebisi",
]

# Corrected score mappings (matches fixed submit_assessment in app.py)
SCORE_MAPPINGS = [
    {1:1,2:2,3:3,4:4,5:5},  # Q1  cheerful        POSITIVE 5-opt
    {1:1,2:2,3:3,4:4,5:5},  # Q2  calm            POSITIVE 5-opt
    {1:1,2:2,3:3,4:4,5:5},  # Q3  active          POSITIVE 5-opt
    {1:1,2:2,3:3,4:4,5:5},  # Q4  rested          POSITIVE 5-opt
    {1:1,2:2,3:3,4:4,5:5},  # Q5  interested      POSITIVE 5-opt
    {1:4,2:3,3:2,4:1},       # Q6  no interest     NEGATIVE 4-opt
    {1:4,2:3,3:2,4:1},       # Q7  depressed       NEGATIVE 4-opt
    {1:5,2:4,3:3,4:2,5:1},  # Q8  concentrate     NEGATIVE 5-opt
    {1:5,2:4,3:3,4:2,5:1},  # Q9  anxious         NEGATIVE 5-opt
    {1:5,2:4,3:3,4:2,5:1},  # Q10 out of control  NEGATIVE 5-opt
    {1:1,2:2,3:3,4:4},       # Q11 safe home       POSITIVE 4-opt
    {1:4,2:3,3:2,4:1},       # Q12 touched         NEGATIVE CRITICAL 4-opt
    {1:4,2:3,3:2,4:1},       # Q13 hurt            NEGATIVE CRITICAL 4-opt
    {1:4,2:3,3:2,4:1},       # Q14 pressured       NEGATIVE 4-opt
    {1:1,2:2,3:3,4:4},       # Q15 can say no      POSITIVE 4-opt
    {1:1,2:2,3:3,4:4},       # Q16 SRH access      POSITIVE 4-opt
    {1:1,2:2,3:3,4:4},       # Q17 SRH needs       4-opt
    {1:1,2:2,3:3,4:4},       # Q18 optimistic      POSITIVE 4-opt
    {1:1,2:2,3:3,4:4},       # Q19 SRH support     POSITIVE 4-opt
    {1:1,2:2,3:3,4:4},       # Q20 knows help      POSITIVE 4-opt
]
MAX_OPTS = [5,5,5,5,5, 4,4,5,5,5, 4,4,4,4,4, 4,4,4,4,4]
NEGATIVE_Q = {5,6,7,8,9, 11,12,13}  # 0-indexed

def make_answers(archetype):
    """Generate 20 question answers weighted by wellness archetype."""
    answers = []
    for idx, mx in enumerate(MAX_OPTS):
        neg = idx in NEGATIVE_Q
        if archetype == "thriving":
            weights = ([5,4,2,1,1] if neg else [1,1,2,4,5])[:mx]
        elif archetype == "mostly_well":
            weights = ([4,3,2,1,1] if neg else [1,2,3,4,3])[:mx]
        elif archetype == "moderate":
            weights = [2,3,4,3,2][:mx]
        elif archetype == "struggling":
            weights = ([1,2,3,4,5] if neg else [5,4,2,1,1])[:mx]
        else:  # critical
            weights = ([1,1,2,4,5] if neg else [5,4,2,1,1])[:mx]
        answers.append(random.choices(range(1, mx+1), weights=weights)[0])
    return answers

def calc_score(answers):
    return sum(SCORE_MAPPINGS[i].get(answers[i], 0) for i in range(20))

def make_person(idx):
    sex   = random.choice(["male", "female"])
    first = random.choice(MALE_FIRST if sex == "male" else FEMALE_FIRST)
    last  = random.choice(LAST_NAMES)
    age   = random.randint(16, 32)
    email = f"{first.lower()}.{last.lower()}{random.randint(1,99)}@gmail.com"
    phone = f"080{random.randint(10000000, 99999999)}"
    arch  = random.choices(
        ["thriving","mostly_well","moderate","struggling","critical"],
        weights=[15, 25, 30, 20, 10]
    )[0]
    answers = make_answers(arch)
    score   = calc_score(answers)
    days_ago = random.randint(0, 180)
    ts = (datetime.now() - timedelta(
        days=days_ago,
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )).strftime("%Y-%m-%d %H:%M:%S")
    return dict(
        timestamp=ts, email=email, phone=phone,
        age=age, sex=sex, score=score,
        **{f"q{i+1}": answers[i] for i in range(20)}
    )

def score_band(s):
    if s >= 70: return "Excellent"
    if s >= 52: return "Good"
    if s >= 35: return "Moderate"
    if s >= 18: return "High Risk"
    return "Critical"

# ── Generate 27 people ────────────────────────────────────────────────────────
people = [make_person(i) for i in range(27)]

# ── INSERT ────────────────────────────────────────────────────────────────────
if USE_FLASK:
    with app.app_context():
        inserted = 0
        skipped  = 0
        for p in people:
            # Skip if email already exists (prevents duplicate runs)
            exists = SubmitAssessment.query.filter_by(email=p["email"]).first()
            if exists:
                skipped += 1
                continue
            record = SubmitAssessment(**p)
            db.session.add(record)
            inserted += 1
        db.session.commit()
        print(f"\n[OK]  Inserted {inserted} records  |  Skipped {skipped} duplicates")
else:
    # Direct SQLite fallback
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    # Check table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='submit_assessment'")
    if not cur.fetchone():
        print("[ERROR] Table 'submit_assessment' not found. Run the Flask app once first to create tables.")
        conn.close()
        sys.exit(1)

    cols = ("timestamp,email,phone,age,sex,score,"
            "q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,"
            "q11,q12,q13,q14,q15,q16,q17,q18,q19,q20")
    placeholders = ",".join(["?"] * 26)
    sql = f"INSERT OR IGNORE INTO submit_assessment ({cols}) VALUES ({placeholders})"

    inserted = skipped = 0
    for p in people:
        row = (
            p["timestamp"], p["email"], p["phone"], p["age"], p["sex"], p["score"],
            p["q1"],p["q2"],p["q3"],p["q4"],p["q5"],
            p["q6"],p["q7"],p["q8"],p["q9"],p["q10"],
            p["q11"],p["q12"],p["q13"],p["q14"],p["q15"],
            p["q16"],p["q17"],p["q18"],p["q19"],p["q20"],
        )
        cur.execute(sql, row)
        if cur.rowcount:
            inserted += 1
        else:
            skipped += 1

    conn.commit()
    conn.close()
    print(f"\n[OK]  Inserted {inserted} records  |  Skipped {skipped} duplicates")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n-- Preview of seeded respondents ------------------------------------------")
print(f"{'#':<3} {'Name':<22} {'Age':<4} {'Sex':<7} {'Score':<8} {'Band'}")
print("-" * 65)
for i, p in enumerate(people, 1):
    name = f"{p['email'].split('.')[0].capitalize()} {p['email'].split('.')[1].split('@')[0].rstrip('0123456789').capitalize()}"
    print(f"{i:<3} {name:<22} {p['age']:<4} {p['sex']:<7} {p['score']:<8} {score_band(p['score'])}")

scores = [p["score"] for p in people]
print(f"\nAvg score : {sum(scores)/len(scores):.1f} / 88")
print(f"Range     : {min(scores)} – {max(scores)}")
print(f"Bands     : ", end="")
for band in ["Critical","High Risk","Moderate","Good","Excellent"]:
    cnt = sum(1 for p in people if score_band(p["score"]) == band)
    if cnt: print(f"{band}={cnt}", end="  ")
print("\n")