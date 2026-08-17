"""
NetSec Console — Day 2 Networking Lab
A local CTF-style lab for practicing networking-for-cloud-security concepts.
Run: python3 app.py   then open http://localhost:5000
"""

import sqlite3
import io
from datetime import datetime, timezone
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)
DB_PATH = "lab.db"

# ---------------------------------------------------------------------------
# Challenge definitions
# ---------------------------------------------------------------------------
CHALLENGES = [
    {
        "id": "ch01",
        "num": "01",
        "category": "RECON",
        "title": "Interface Recon",
        "objective": "Identify your machine's network interface and local IP address.",
        "commands": ["ip addr"],
        "task": "Run the command above in your terminal. Find your primary network "
                "interface name (e.g. eth0, wlan0) and its assigned local IP address.",
        "prompt": "Paste your interface name and local IP address (e.g. 'eth0 - 172.20.10.4').",
        "hint": "Look for the interface that has 'state UP' and an inet line that isn't 127.0.0.1.",
    },
    {
        "id": "ch02",
        "num": "02",
        "category": "RECON",
        "title": "DNS Resolution",
        "objective": "See DNS convert a domain name into an IP address.",
        "commands": ["nslookup google.com"],
        "task": "Run the command above. Note the IP address(es) returned. Then explain: "
                "what job does DNS do for a cloud service like AWS Route 53?",
        "prompt": "Paste the resolved IP address, and your one-line explanation of DNS's role in cloud.",
        "hint": "If nslookup isn't installed, try 'dig google.com' instead.",
    },
    {
        "id": "ch03",
        "num": "03",
        "category": "RECON",
        "title": "HTTPS Handshake Check",
        "objective": "Inspect HTTP response headers over HTTPS (port 443).",
        "commands": ["curl -I https://google.com"],
        "task": "Run the command above. Report the HTTP status code and the 'server' header "
                "if present. What does HTTPS traffic tell you about what's happening on port 443?",
        "prompt": "Paste the status code + server header, and your note on port 443 / HTTPS.",
        "hint": "-I sends a HEAD request so you only see headers, not the full page body.",
    },
    {
        "id": "ch04",
        "num": "04",
        "category": "RECON",
        "title": "Path Trace",
        "objective": "See the network hops your traffic takes to reach a destination.",
        "commands": ["traceroute google.com", "sudo apt install traceroute   # if missing"],
        "task": "Run traceroute against google.com. Report roughly how many hops your "
                "traffic passed through before reaching the destination.",
        "prompt": "How many hops (approx), and one line on why this matters for network security.",
        "hint": "Each numbered line is one hop (one router your packet passed through).",
    },
    {
        "id": "ch05",
        "num": "05",
        "category": "RECON",
        "title": "Port Watch",
        "objective": "Find which ports your own machine is listening on.",
        "commands": ["ss -tulnp", "netstat -tulnp   # fallback if ss unavailable"],
        "task": "Run the command above. List at least two listening ports/services you find, "
                "and for each, note whether it's TCP or UDP.",
        "prompt": "List 2+ ports/services found and their protocol (TCP/UDP).",
        "hint": "-t = TCP, -u = UDP, -l = listening only, -n = numeric, -p = show process name.",
    },
    {
        "id": "ch06",
        "num": "06",
        "category": "CONCEPT",
        "title": "TCP vs UDP",
        "objective": "Understand the core tradeoff between the two main transport protocols.",
        "commands": [],
        "task": "No command for this one. In your own words, explain the core difference "
                "between TCP and UDP, and give one real example of when a cloud application "
                "would use each.",
        "prompt": "Your explanation of TCP vs UDP + one real-world example of each.",
        "hint": "Think: reliability + ordering (TCP) vs speed + no guarantee (UDP). DNS, video calls, gaming often use UDP.",
    },
    {
        "id": "ch07",
        "num": "07",
        "category": "CONCEPT",
        "title": "Port 22 Exposure",
        "objective": "Understand why SSH exposure is a classic cloud misconfiguration.",
        "commands": [],
        "task": "Explain in your own words why leaving port 22 (SSH) open to 0.0.0.0/0 "
                "(the entire internet) on an AWS EC2 instance is dangerous, and what you'd "
                "do instead to secure it.",
        "prompt": "Your explanation + the fix you'd apply (e.g. restrict source IP, bastion host, etc.).",
        "hint": "Think about brute-force attempts, and how Security Groups can restrict source IP ranges.",
    },
    {
        "id": "ch08",
        "num": "08",
        "category": "CONCEPT",
        "title": "Security Group vs NACL",
        "objective": "Distinguish AWS's two firewall layers.",
        "commands": [],
        "task": "Explain the difference between an AWS Security Group and a Network ACL (NACL) — "
                "specifically: stateful vs stateless, and instance-level vs subnet-level.",
        "prompt": "Your comparison of Security Group vs NACL.",
        "hint": "Stateful = return traffic auto-allowed. Stateless = you must explicitly allow both directions.",
    },
    {
        "id": "ch09",
        "num": "09",
        "category": "CONCEPT",
        "title": "NAT Gateway Logic",
        "objective": "Understand outbound-only internet access for private resources.",
        "commands": [],
        "task": "Explain why a private-subnet resource (e.g. a database) would need a NAT "
                "Gateway to reach the internet for things like updates, but should never be "
                "given a public IP directly.",
        "prompt": "Your explanation of NAT's role and why private resources avoid public IPs.",
        "hint": "NAT allows outbound-initiated traffic out, but blocks unsolicited inbound connections in.",
    },
    {
        "id": "ch10",
        "num": "10",
        "category": "CONCEPT",
        "title": "DNS in Cloud Security",
        "objective": "See DNS as an attack surface, not just a lookup service.",
        "commands": [],
        "task": "Explain one way DNS can be abused or attacked (e.g. DNS hijacking, subdomain "
                "takeover, cache poisoning), and why this matters specifically for cloud-hosted apps.",
        "prompt": "Name the attack type + why it matters in a cloud context.",
        "hint": "Think about what happens if an attacker points your subdomain's DNS record at infrastructure they control.",
    },
]

CHALLENGE_MAP = {c["id"]: c for c in CHALLENGES}


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            challenge_id TEXT PRIMARY KEY,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS day_status (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            completed INTEGER NOT NULL DEFAULT 0,
            completed_at TEXT
        )
    """)
    conn.execute("INSERT OR IGNORE INTO day_status (id, completed) VALUES (1, 0)")
    conn.commit()
    conn.close()


def now_iso():
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    conn = get_db()
    rows = conn.execute("SELECT * FROM answers").fetchall()
    status = conn.execute("SELECT * FROM day_status WHERE id = 1").fetchone()
    conn.close()

    answers = {r["challenge_id"]: r["answer"] for r in rows}
    answered_count = len(answers)

    return render_template(
        "index.html",
        challenges=CHALLENGES,
        answers=answers,
        answered_count=answered_count,
        total_count=len(CHALLENGES),
        day_completed=bool(status["completed"]),
    )


@app.route("/api/answer", methods=["POST"])
def save_answer():
    data = request.get_json(force=True)
    challenge_id = data.get("challenge_id")
    answer_text = (data.get("answer") or "").strip()

    if challenge_id not in CHALLENGE_MAP:
        return jsonify({"ok": False, "error": "Unknown challenge"}), 400
    if not answer_text:
        return jsonify({"ok": False, "error": "Answer cannot be empty"}), 400

    conn = get_db()
    existing = conn.execute(
        "SELECT * FROM answers WHERE challenge_id = ?", (challenge_id,)
    ).fetchone()

    ts = now_iso()
    if existing:
        conn.execute(
            "UPDATE answers SET answer = ?, updated_at = ? WHERE challenge_id = ?",
            (answer_text, ts, challenge_id),
        )
    else:
        conn.execute(
            "INSERT INTO answers (challenge_id, answer, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (challenge_id, answer_text, ts, ts),
        )
    conn.commit()

    answered_count = conn.execute("SELECT COUNT(*) c FROM answers").fetchone()["c"]
    conn.close()

    return jsonify({
        "ok": True,
        "answered_count": answered_count,
        "total_count": len(CHALLENGES),
    })


@app.route("/api/complete_day", methods=["POST"])
def complete_day():
    conn = get_db()
    conn.execute(
        "UPDATE day_status SET completed = 1, completed_at = ? WHERE id = 1",
        (now_iso(),),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/export")
def export_answers():
    conn = get_db()
    rows = conn.execute("SELECT * FROM answers").fetchall()
    status = conn.execute("SELECT * FROM day_status WHERE id = 1").fetchone()
    conn.close()

    answers = {r["challenge_id"]: r["answer"] for r in rows}

    lines = []
    lines.append("# Day 2 — Networking for Cloud Security — Lab Answers")
    lines.append("")
    lines.append(f"Exported: {now_iso()}")
    lines.append(f"Progress: {len(answers)}/{len(CHALLENGES)} challenges answered")
    lines.append(f"Day marked complete: {'Yes' if status['completed'] else 'No'}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for c in CHALLENGES:
        lines.append(f"## [{c['num']}] {c['title']} ({c['category']})")
        lines.append("")
        lines.append(f"**Objective:** {c['objective']}")
        if c["commands"]:
            lines.append("")
            lines.append("**Commands used:**")
            for cmd in c["commands"]:
                lines.append(f"```\n{cmd}\n```")
        lines.append("")
        lines.append(f"**Task:** {c['task']}")
        lines.append("")
        ans = answers.get(c["id"])
        if ans:
            lines.append("**My answer:**")
            lines.append("")
            lines.append(ans)
        else:
            lines.append("**My answer:** _(not answered)_")
        lines.append("")
        lines.append("---")
        lines.append("")

    content = "\n".join(lines)
    buf = io.BytesIO(content.encode("utf-8"))
    buf.seek(0)

    return send_file(
        buf,
        mimetype="text/markdown",
        as_attachment=True,
        download_name="day2-networking-answers.md",
    )


if __name__ == "__main__":
    init_db()
    print("\n  NetSec Console running -> http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
