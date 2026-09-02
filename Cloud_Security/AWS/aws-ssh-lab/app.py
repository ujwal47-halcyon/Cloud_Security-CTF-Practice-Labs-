"""
AWS EC2 SSH Hardening Lab - Intentionally Vulnerable Application
For educational purposes only - Do NOT deploy to production!

This lab simulates SSH hardening challenges for AWS EC2 instances.
Students will identify and exploit misconfigurations to find flags.
"""

from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

# Mock AWS EC2 Instance Configuration
MOCK_INSTANCES = {
    "i-0a1b2c3d4e5f6g7h8": {
        "name": "web-server-prod",
        "ip": "10.0.1.50",
        "public_ip": "54.210.100.200",
        "os": "Ubuntu 22.04",
        "ssh_hardening": {
            "port": 22,
            "protocol": "TCP",
            "allowed_ips": ["0.0.0.0/0"],  # VULNERABILITY: Open to all
            "key_based_only": True,
            "password_auth": True,  # VULNERABILITY: Password auth enabled
            "fail2ban": False,  # VULNERABILITY: Fail2Ban disabled
            "permit_root_login": True,  # VULNERABILITY: root login permitted
            "allowed_users": ["ubuntu", "admin", "root"],  # VULNERABILITY: root in list
        },
        "flags": [],
    }
}

# Challenge Definitions
CHALLENGES = {
    "ssh-l1": {
        "title": "SSH Port Misconfiguration",
        "type": "critical",
        "description": "The SSH service is exposed on the default port 22 to the internet. Find evidence of this misconfiguration.",
        "hint": "Check the security group or instance configuration for SSH port exposure",
        "flag_key": "default_port_exposed"
    },
    "ssh-l2": {
        "title": "Password Authentication Enabled",
        "type": "high",
        "description": "SSH is configured to allow password authentication. Identify this weakness and find the default credentials.",
        "hint": "Look for SSH daemon configuration or authentication settings",
        "flag_key": "password_auth_warning"
    },
    "ssh-l3": {
        "title": "Root Login Permitted",
        "type": "high",
        "description": "The SSH server allows direct root login. Find the configuration that permits this dangerous practice.",
        "hint": "Check PermitRootLogin setting in SSH config",
        "flag_key": "root_login_issue"
    },
    "ssh-l4": {
        "title": "Fail2Ban Not Enabled",
        "type": "medium",
        "description": "No intrusion prevention system is configured. Find evidence that fail2ban is not installed or active.",
        "hint": "Check for intrusion prevention tools",
        "flag_key": "fail2ban_missing"
    },
    "ssh-l5": {
        "title": "Security Group Overly Permissive",
        "type": "critical",
        "description": "The security group allows SSH from 0.0.0.0/0 (any IP). Document this severe misconfiguration.",
        "hint": "Examine the effective security group rules",
        "flag_key": "sg_open_to_internet"
    }
}

# HTML Templates
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AWS EC2 SSH Hardening Lab</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .challenge { background: #f9f9f9; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }
        .vulnerable { border-left-color: #f44336; }
        .code { background: #2d2d2d; color: #fff; padding: 10px; border-radius: 4px; overflow-x: auto; }
        a { color: #2196F3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 AWS EC2 SSH Hardening Lab</h1>
        <p><strong>Educational Purpose Only</strong> - Do NOT deploy to production!</p>

        <h2>📋 Available Challenges</h2>
        {% for challenge_id, challenge in challenges.items() %}
        <div class="challenge {% if challenge.type == 'critical' %}vulnerable{% endif %}">
            <h3>{{ challenge.title }} <span style="color: #f44336;">[{{ challenge.type }}]</span></h3>
            <p>{{ challenge.description }}</p>
            <p><em>Hint: {{ challenge.hint }}</em></p>
            <p><strong>Challenge ID:</strong> <code>{{ challenge_id }}</strong></p>
        </div>
        {% endfor %}

        <h2>🔧 Quick Actions</h2>
        <ul>
            <li><a href="/api/instance/i-0a1b2c3d4e5f6g7h8">Get Instance Details</a></li>
            <li><a href="/api/config">View SSH Config (Vulnerable)</a></li>
            <li><a href="/api/logs">View SSH Logs</a></li>
        </ul>

        <h2>⚠️ Security Issues Found</h2>
        <ul>
            <li>SSH on default port 22 exposed to internet</li>
            <li>Password authentication enabled</li>
            <li>Root login permitted</li>
            <li>No fail2ban protection</li>
            <li>Security group 0.0.0.0/0 allows all IPs</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE, challenges=CHALLENGES)


@app.route("/api/instance/<instance_id>")
def get_instance(instance_id):
    """API endpoint to get instance details - VULNERABLE: Exposes full SSH config"""
    if instance_id in MOCK_INSTANCES:
        return jsonify(MOCK_INSTANCES[instance_id])
    return jsonify({"error": "Instance not found"}), 404


@app.route("/api/config", methods=["GET"])
def get_ssh_config():
    """Get SSH configuration - INTENTIONALLY VULNERABLE"""
    return jsonify({
        "/etc/ssh/sshd_config": """
# SSH Server Configuration File
# Danger: This configuration has multiple security issues

# Includedir /etc/ssh/sshd_config.d

Port 22
PermitRootLogin yes
PasswordAuthentication yes
PermitEmptyPasswords no
ChallengeResponseAuthentication no
X11Forwarding yes
PrintMotd no
TCPKeepAlive yes
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server

# WARNING: No Fail2Ban protection!
# WARNING: Root login is permitted!
# WARNING: Password auth is enabled!
"""
    })


@app.route("/api/logs", methods=["GET"])
def get_simulated_logs():
    """Simulated SSH logs showing potential attacks"""
    return jsonify({
        "logs": [
            {"timestamp": "2026-09-01T10:00:00Z", "message": "Accepted publickey for ubuntu from 192.168.1.100 port 52341"},
            {"timestamp": "2026-09-01T10:05:00Z", "message": "Failed password for root from 10.0.0.50 port 43210"},
            {"timestamp": "2026-09-01T10:05:05Z", "message": "Failed password for root from 10.0.0.50 port 43211"},
            {"timestamp": "2026-09-01T10:05:10Z", "message": "Failed password for root from 10.0.0.50 port 43212"},
        ],
        "note": "Multiple failed root login attempts - no rate limiting detected"
    })


@app.route("/api/flags", methods=["POST"])
def submit_flags():
    """Submit findings to get flags"""
    data = request.get_json() or {}

    # Expected evidence for each challenge (case-insensitive matching)
    evidence_map = {
        "ssh-l1": ["default port", "port 22", "ssh", "exposed", "open"],
        "ssh-l2": ["password", "permitted", "passwordauth"],
        "ssh-l3": ["permitrootlogin", "root login"],
        "ssh-l4": ["fail2ban", "intrusion"],
        "ssh-l5": ["0.0.0.0/0", "overly permissive", "security group"]
    }

    results = []
    flags = {
        "ssh-l1": "SSH-DEFAULT-PORT-CONFIG-VULN",
        "ssh-l2": "SSH-PASSWORD-AUTH-ENABLED-INFO",
        "ssh-l3": "SSH-ROOT-LOGIN-PERMITTED-DANGER",
        "ssh-l4": "SSH-FAIL2BAN-NOT-INSTALLED",
        "ssh-l5": "SSH-SG-0.0.0.0-0-CIDR-VIOLATION"
    }

    evidence = data.get("evidence", "")

    for challenge_id, required_terms in evidence_map.items():
        matched = any(term.lower() in evidence.lower() for term in required_terms)
        if matched:
            results.append({
                "challenge": challenge_id,
                "title": CHALLENGES[challenge_id]["title"],
                "flag": flags[challenge_id],
                "status": "success"
            })

    return jsonify({"results": results})


@app.route("/admin")
def admin():
    """Admin panel showing instance vulnerabilities"""
    admin_template = """
    <!DOCTYPE html>
    <html>
    <head><title>Admin - SSH Lab</title></head>
    <body>
        <h1>Admin Dashboard</h1>
        <h2>Detected Security Issues</h2>
        <ul>
            <li>Port 22 open to 0.0.0.0/0</li>
            <li>PasswordAuthentication yes</li>
            <li>PermitRootLogin yes</li>
        </ul>
    </body>
    </html>
    """
    return render_template_string(admin_template)


if __name__ == "__main__":
    print("=" * 60)
    print("🔥 AWS EC2 SSH Hardening Lab")
    print("📍 URL: http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)