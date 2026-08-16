# ✅ Linux Fundamentals CTF Lab — Solutions

> ⚠️ **SPOILER WARNING — only read this AFTER finishing all 10 levels.**
> If you read it early you'll cheat yourself out of the practice.

## Level 1 — `ls`, `cd`, `cat`
```
ls
cat note3.txt
```
**Flag:** `CTF{cat_is_your_friend}`
**Learned:** list files, change directories, read files.

## Level 2 — Hidden files
```
ls -la
cat .secret
```
**Flag:** `CTF{hidden_things_hide}`
**Learned:** hidden files start with `.`; `ls -la` reveals them.

## Level 3 — `find`
```
find . -type f -name "*.txt"
```
**Flag:** `CTF{find_me_everywhere}`
**Learned:** `find` searches a directory tree recursively.

## Level 4 — `grep`
```
grep "CTF" log.txt
```
**Flag:** `CTF{grep_is_magic}`
**Learned:** `grep` searches inside files instead of reading them all.

## Level 5 — Permissions
```
ls -l
find . -type f -executable
./run.sh
```
**Flag:** `CTF{permissions_matter}`
**Learned:** the `x` bit = execute; run scripts with `./`.

## Level 6 — `tar`
```
tar -tzf archive.tar.gz
tar -xzf archive.tar.gz
cat flag.txt
```
**Flag:** `CTF{tar_time_archives}`
**Learned:** list (`-t`) and extract (`-x`) archives with `tar`.

## Level 7 — `base64`
```
base64 -d encoded.txt
```
**Flag:** `CTF{encoding_is_not_encryption}`
**Learned:** base64 is reversible encoding, not encryption.

## Level 8 — `strings`
```
strings binary | grep CTF
```
**Flag:** `CTF{strings_reveal_all}`
**Learned:** `strings` extracts readable text from binary files.

## Level 9 — Symlinks
```
ls -la
cat flag_link
readlink flag_link
```
**Flag:** `CTF{symlinks_point_the_way}`
**Learned:** a symlink is a shortcut; reading it reads its target.

## Level 10 — Wildcards + environment
```
cat *flag*.txt
echo $USER
printenv | head
```
**Flag:** `CTF{you_conquered_linux}`
**Learned:** `*` matches patterns; environment lives in variables.

---

## Why this matters for cloud security

Every one of these commands is used daily in cloud security:
- `grep`/`find` → searching logs and files on Linux servers
- `tar`/`base64`/`strings` → triaging malware, decoding payloads
- permissions → understanding file/OS security
- symlinks → part of Linux privilege-escalation attacks
- environment variables → where cloud creds often leak
