# 🔒 AWS EC2 SSH Hardening Lab

This lab provides hands-on practice for identifying, exploiting, and remediating insecure SSH configurations on AWS EC2 instances.

## ⚠️ Important Disclaimer
For educational and training purposes only. Never expose vulnerable SSH configurations to public-facing networks.

---

## 🚀 How to Set Up and Run on AWS / Local Windows PowerShell

### Step 1: Open PowerShell on Windows
Open Windows PowerShell and navigate to your lab directory:
```powershell
cd C:\Users\Ujwal\Desktop\AI\aws-ssh-lab
```

### Step 2: Install Dependencies
Ensure Python 3 and Flask are installed:
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Run the Lab Application
```powershell
python app.py
```
Open your browser at: `http://localhost:5000`

---

## 🛠️ How to Deploy an Actual EC2 Instance for SSH Hardening

If you want to practice real SSH hardening on AWS EC2 (Free Tier):

1. **Launch EC2 Instance**:
   - AMI: Ubuntu 22.04 LTS (Free Tier eligible)
   - Instance Type: `t2.micro` or `t3.micro`
   - Key Pair: Create a new `.pem` key pair (e.g., `ssh-lab-key.pem`)

2. **Configure Security Group (INTENTIONALLY INSECURE FOR LAB)**:
   - Type: `SSH`
   - Port: `22`
   - Source: `0.0.0.0/0` (Allows anyone to connect — **misconfiguration to fix!**)

3. **Connect via PowerShell**:
   ```powershell
   # Fix private key permissions on Windows if needed
   icacls "ssh-lab-key.pem" /inheritance:r
   icacls "ssh-lab-key.pem" /grant:r "$($env:USERNAME):(R)"

   # SSH into the instance
   ssh -i "ssh-lab-key.pem" ubuntu@<YOUR_EC2_PUBLIC_IP>
   ```

---

## 🔍 Lab Challenges & Exploitation Guide

### Challenge 1: Identify Port 22 Exposure
- **Vulnerability**: SSH runs on default port 22 exposed to `0.0.0.0/0`.
- **Exploitation / Audit**:
  ```bash
  sudo ss -tulpn | grep sshd
  ```
- **Remediation**: Change the default SSH port in `/etc/ssh/sshd_config` (e.g., `Port 2222`).

### Challenge 2: Password Authentication Enabled
- **Vulnerability**: `PasswordAuthentication yes` allows brute-forcing.
- **Exploitation**: Try logging in with incorrect/common passwords.
- **Remediation**: Set `PasswordAuthentication no` and enforce SSH keys.

### Challenge 3: Direct Root Login Permitted
- **Vulnerability**: `PermitRootLogin yes` allows direct root compromise.
- **Exploitation**: Attempting SSH login as `root`.
- **Remediation**: Set `PermitRootLogin no` and use sudo via a regular user.

### Challenge 4: Missing Intrusion Prevention (Fail2Ban)
- **Vulnerability**: No automated blocking of brute-force IPs.
- **Exploitation**: Run failed login attempts; notice no blocking occurs.
- **Remediation**: Install and configure `fail2ban`.

### Challenge 5: Overly Permissive Security Group
- **Vulnerability**: Security Group allows SSH from `0.0.0.0/0`.
- **Exploitation**: Anyone on the internet can attempt connections.
- **Remediation**: Restrict SSH inbound rule to your specific IP address (`/32`).
