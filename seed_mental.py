# -*- coding: utf-8 -*-
"""
seed_mental_db.py
-----------------
Run this from the ROOT of your Flask project (same folder as app.py):

    python seed_mental_db.py

It will insert 350 Yoruba-named respondents directly into your
submit-assessment.db SQLite database using the corrected scoring logic.
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ── Project Setup ─────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

USE_FLASK = True
try:
    from app import app, db, SubmitAssessment
except Exception as e:
    print(f"[INFO] Could not import Flask app ({e}). Using direct SQLite insert.")
    USE_FLASK = False

if not USE_FLASK:
    import sqlite3
    DB_CANDIDATES = ["instance/submit-assessment.db", "submit-assessment.db", "instance/default.db"]
    DB_PATH = next((p for p in DB_CANDIDATES if os.path.exists(p)), None)
    if DB_PATH is None:
        print("[ERROR] Could not find submit-assessment.db.")
        sys.exit(1)
    print(f"[INFO] Using database: {DB_PATH}")

# ── Extended Seed Data ────────────────────────────────────────────────────────
random.seed(42) # Changed seed for fresh variety

MALE_FIRST = [
    "Adewale", "Babatunde", "Damilola", "Femi", "Gbenga", "Idris", "Jide", "Kayode", "Leke", "Muyiwa",
    "Niyi", "Oluwaseun", "Pelumi", "Rotimi", "Segun", "Taiwo", "Usman", "Kunle", "Wole", "Tunde",
    "Abiodun", "Adekunle", "Ayodeji", "Bolaji", "Bukola", "Eniola", "Folarin", "Gboyega", "Ifeanyi",
    "Kazeem", "Lanre", "Modupe", "Olumide", "Seyi", "Tokunbo", "Yemi", "Yinka"
]

FEMALE_FIRST = [
    "Adaeze", "Blessing", "Chiamaka", "Folake", "Grace", "Halima", "Ifeoma", "Jumoke", "Kehinde", "Latifat",
    "Morenike", "Ngozi", "Omolara", "Ronke", "Sade", "Titilayo", "Uche", "Yetunde", "Bimpe", "Tosin",
    "Adesua", "Anuoluwapo", "Bisi", "Bunmi", "Damilare", "Enitan", "Funmilayo", "Ibukun", "Moji",
    "Nike", "Olaide", "Opeyemi", "Simisola", "Temitope", "Wuraola", "Zainab"
]

LAST_NAMES = [
    "Adeyemi", "Babatunde", "Okonkwo", "Adeleke", "Okafor", "Adesanya", "Ogunleye", "Balogun", "Adeola", "Fashola",
    "Oluwole", "Afolabi", "Gbadamosi", "Ojo", "Salami", "Akintola", "Odunsi", "Agboola", "Ijiwola", "Adebisi",
    "Abiola", "Ajayi", "Akande", "Alabi", "Bankole", "Daramola", "Egunjobi", "Falade", "Ishola", "Lawal",
    "Obasanjo", "Oyelowo", "Popoola", "Shonibare", "Tinubu", "Williams", "Yerima"
]

# Scoring Config
SCORE_MAPPINGS = [
    {1:1,2:2,3:3,4:4,5:5}, {1:1,2:2,3:3,4:4,5:5}, {1:1,2:2,3:3,4:4,5:5}, {1:1,2:2,3:3,4:4,5:5}, {1:1,2:2,3:3,4:4,5:5},
    {1:4,2:3,3:2,4:1}, {1:4,2:3,3:2,4:1}, {1:5,2:4,3:3,4:2,5:1}, {1:5,2:4,3:3,4:2,5:1}, {1:5,2:4,3:3,4:2,5:1},
    {1:1,2:2,3:3,4:4}, {1:4,2:3,3:2,4:1}, {1:4,2:3,3:2,4:1}, {1:4,2:3,3:2,4:1}, {1:1,2:2,3:3,4:4},
    {1:1,2:2,3:3,4:4}, {1:1,2:2,3:3,4:4}, {1:1,2:2,3:3,4:4}, {1:1,2:2,3:3,4:4}, {1:1,2:2,3:3,4:4}
]
MAX_OPTS = [5,5,5,5,5, 4,4,5,5,5, 4,4,4,4,4, 4,4,4,4,4]
NEGATIVE_Q = {5,6,7,8,9, 11,12,13}

def make_answers(archetype):
    answers = []
    for idx, mx in enumerate(MAX_OPTS):
        neg = idx in NEGATIVE_Q
        if archetype == "thriving": weights = ([5,4,2,1,1] if neg else [1,1,2,4,5])[:mx]
        elif archetype == "mostly_well": weights = ([4,3,2,1,1] if neg else [1,2,3,4,3])[:mx]
        elif archetype == "moderate": weights = [2,3,4,3,2][:mx]
        elif archetype == "struggling": weights = ([1,2,3,4,5] if neg else [5,4,2,1,1])[:mx]
        else: weights = ([1,1,2,4,5] if neg else [5,4,2,1,1])[:mx]
        answers.append(random.choices(range(1, mx+1), weights=weights)[0])
    return answers

def calc_score(answers):
    return sum(SCORE_MAPPINGS[i].get(answers[i], 0) for i in range(20))

def make_person(idx):
    sex   = random.choice(["male", "female"])
    first = random.choice(MALE_FIRST if sex == "male" else FEMALE_FIRST)
    last  = random.choice(LAST_NAMES)
    age   = random.randint(16, 35)
    # Ensure unique emails by using index
    email = f"{first.lower()}.{last.lower()}{idx}@mentalhealth.ng"
    phone = f"080{random.randint(10000000, 99999999)}"
    arch  = random.choices(
        ["thriving","mostly_well","moderate","struggling","critical"],
        weights=[10, 25, 35, 20, 10]
    )[0]
    answers = make_answers(arch)
    score   = calc_score(answers)
    ts = (datetime.now() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))).strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "timestamp": ts, "email": email, "phone": phone, "age": age, "sex": sex, "score": score
    }
    for i in range(20):
        data[f"q{i+1}"] = answers[i]
    return data

def score_band(s):
    if s >= 70: return "Excellent"
    if s >= 52: return "Good"
    if s >= 35: return "Moderate"
    if s >= 18: return "High Risk"
    return "Critical"

# ── Generate 350 people ───────────────────────────────────────────────────────
people = [make_person(i) for i in range(350)]

# ── INSERTION LOGIC ───────────────────────────────────────────────────────────
if USE_FLASK:
    with app.app_context():
        inserted = 0
        skipped  = 0
        for p in people:
            exists = SubmitAssessment.query.filter_by(email=p["email"]).first()
            if exists:
                skipped += 1
                continue
            record = SubmitAssessment(**p)
            db.session.add(record)
            inserted += 1
        db.session.commit()
else:
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cols = ("timestamp,email,phone,age,sex,score," + ",".join([f"q{i+1}" for i in range(20)]))
    placeholders = ",".join(["?"] * 26)
    sql = f"INSERT OR IGNORE INTO submit_assessment ({cols}) VALUES ({placeholders})"
    
    data_tuples = [tuple(p.values()) for p in people]
    cur.executemany(sql, data_tuples)
    inserted = cur.rowcount
    skipped = 350 - inserted
    conn.commit()
    conn.close()

print(f"\n[OK] Processed 350 records: {inserted} inserted, {skipped} skipped.")

# ── Summary Statistics ────────────────────────────────────────────────────────
print("\n-- Demographic Summary ----------------------------------------------------")
scores = [p["score"] for p in people]
for band in ["Critical","High Risk","Moderate","Good","Excellent"]:
    cnt = sum(1 for p in people if score_band(p["score"]) == band)
    print(f"{band:<10}: {cnt} ({ (cnt/350)*100:.1f}%)")

print(f"\nAverage Score: {sum(scores)/350:.1f} / 88")