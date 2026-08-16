"""
Linux Fundamentals CTF — Local Flag Submission Portal

Solve challenges in WSL Kali, then submit flags here in the browser
the same way you do on your other CTF web apps.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://localhost:5000
"""

import json
import os
import secrets
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
os.makedirs(DATA_DIR, exist_ok=True)

CHALLENGES = [
    {
        "id": 1,
        "title": "Read the notes",
        "skill": "ls, cd, cat",
        "hint": "There are a few note files. Read all of them.",
        "flag": "CTF{cat_is_your_friend}",
    },
    {
        "id": 2,
        "title": "Hidden files",
        "skill": "ls -la",
        "hint": "Hidden files start with a dot. List everything.",
        "flag": "CTF{hidden_things_hide}",
    },
    {
        "id": 3,
        "title": "Buried in the tree",
        "skill": "find",
        "hint": "Do not click through folders one by one. Search the tree.",
        "flag": "CTF{find_me_everywhere}",
    },
    {
        "id": 4,
        "title": "Needle in a log",
        "skill": "grep",
        "hint": "Do not cat the whole log. Search inside it.",
        "flag": "CTF{grep_is_magic}",
    },
    {
        "id": 5,
        "title": "Permissions",
        "skill": "ls -l, chmod, ./script",
        "hint": "Look for a file with execute permission and run it.",
        "flag": "CTF{permissions_matter}",
    },
    {
        "id": 6,
        "title": "Archives",
        "skill": "tar",
        "hint": "List the archive first, then extract it.",
        "flag": "CTF{tar_time_archives}",
    },
    {
        "id": 7,
        "title": "Encoded, not encrypted",
        "skill": "base64",
        "hint": "Decode the encoded file. Encoding is reversible.",
        "flag": "CTF{encoding_is_not_encryption}",
    },
    {
        "id": 8,
        "title": "Binary junk",
        "skill": "strings",
        "hint": "cat will look like garbage. Pull readable text out.",
        "flag": "CTF{strings_reveal_all}",
    },
    {
        "id": 9,
        "title": "The shortcut",
        "skill": "symlinks",
        "hint": "A symlink points at another file. Follow it.",
        "flag": "CTF{symlinks_point_the_way}",
    },
    {
        "id": 10,
        "title": "Wildcards + environment",
        "skill": "*, env",
        "hint": "Match files by pattern, then inspect your environment.",
        "flag": "CTF{you_conquered_linux}",
    },
]

FLAG_LOOKUP = {item["flag"].strip().lower(): item for item in CHALLENGES}


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as handle:
                data = json.load(handle)
                if isinstance(data, dict) and "solved" in data:
                    return data
        except Exception:
            pass
    return {"solved": [], "history": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as handle:
        json.dump(progress, handle, indent=2)


def normalize_flag(value):
    return (value or "").strip()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/challenges")
def challenges():
    progress = load_progress()
    solved_ids = set(progress.get("solved", []))
    return render_template(
        "challenges.html",
        challenges=CHALLENGES,
        solved_ids=solved_ids,
        solved_count=len(solved_ids),
        total=len(CHALLENGES),
    )


@app.route("/flags", methods=["GET", "POST"])
def flags():
    progress = load_progress()
    solved_ids = set(progress.get("solved", []))
    message = None
    status = None

    if request.method == "POST":
        submitted = normalize_flag(request.form.get("flag", ""))
        match = FLAG_LOOKUP.get(submitted.lower())

        if not submitted:
            status = "error"
            message = "Paste a flag first."
        elif not match:
            status = "error"
            message = "Not a recognized flag. Keep looking in the terminal."
        elif match["id"] in solved_ids:
            status = "info"
            message = f"Already solved: Level {match['id']} — {match['title']}"
        else:
            progress["solved"].append(match["id"])
            progress["history"].append(
                {
                    "level": match["id"],
                    "title": match["title"],
                    "flag": match["flag"],
                    "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            save_progress(progress)
            solved_ids.add(match["id"])
            status = "success"
            message = f"Correct! Level {match['id']} solved: {match['title']}"

        if len(solved_ids) == len(CHALLENGES) and status == "success":
            message = "All 10 flags captured. Linux fundamentals complete."

    return render_template(
        "flags.html",
        challenges=CHALLENGES,
        solved_ids=solved_ids,
        solved_count=len(solved_ids),
        total=len(CHALLENGES),
        message=message,
        status=status,
    )


@app.route("/reset", methods=["POST"])
def reset():
    save_progress({"solved": [], "history": []})
    return redirect(url_for("flags"))


if __name__ == "__main__":
    print()
    print("=" * 58)
    print("  Linux Fundamentals CTF — Flag Submission Portal")
    print("=" * 58)
    print("  Solve levels in WSL Kali, then submit flags here.")
    print()
    print("  URL:  http://localhost:5000")
    print("  Flags page: http://localhost:5000/flags")
    print()
    print("  Lab folder (Windows):")
    print("    C:\\Users\\Ujwal\\Downloads\\cloud Security\\linux\\linux-ctf-lab")
    print("  Lab folder (WSL):")
    print('    /mnt/c/Users/Ujwal/Downloads/cloud Security/linux/linux-ctf-lab')
    print()
    print("  Build the lab in Kali first:")
    print("    bash setup_lab.sh")
    print("    cd ~/linux-ctf/level1 && ls")
    print("=" * 58)
    print()
    app.run(host="0.0.0.0", port=5000, debug=True)
