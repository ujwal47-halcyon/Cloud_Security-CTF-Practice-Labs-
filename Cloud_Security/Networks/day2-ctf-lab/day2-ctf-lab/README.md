# NetSec Console — Day 2 Lab

A local, self-hosted CTF-style lab for Day 2: Networking for Cloud Security.
10 challenges (5 hands-on recon tasks + 5 concept tasks), each with exact
commands, a task prompt, an optional hint, and a place to log your answer.
Nothing is auto-graded — you log your findings here, export them, and hand
the export to Claude at the end of the day for review.

## Setup (WSL / Kali / any Linux terminal)

```bash
# 1. Unzip this folder somewhere convenient, then cd into it
cd day2-ctf-lab

# 2. Install Flask (only needs to be done once)
pip install flask --break-system-packages

# 3. Run the app
python3 app.py
```

Then open **http://localhost:5000** in your browser.

## How to use it

1. Pick a challenge from the left sidebar.
2. Run the listed command(s) in a **separate terminal window** (WSL, Kali, or
   Windows Terminal — whatever you're already using).
3. Read the task, do the research, and type your answer/finding into the box.
4. Click **Save Answer** — the sidebar dot turns solid once logged.
5. Repeat for all 10 challenges (5 RECON, 5 CONCEPT).
6. When you're done, click **↓ Export** — this downloads
   `day2-networking-answers.md`, a clean write-up of every question + your answer.
7. Click **Mark Day Complete** to close out the day in the app.
8. Upload/paste `day2-networking-answers.md` to Claude — that's the signal to
   review your answers, correct anything wrong, and generate Day 3.

## Notes

- Your answers persist in a local SQLite file (`lab.db`) — closing the
  browser or restarting the app won't lose your progress. It's created
  automatically on first run.
- `traceroute` and `nslookup`/`dig` may need installing if missing:
  `sudo apt install traceroute dnsutils`
- This app only runs on `localhost` — it's not exposed to your network or
  the internet.
- To reset progress and start fresh, stop the app and delete `lab.db`.
