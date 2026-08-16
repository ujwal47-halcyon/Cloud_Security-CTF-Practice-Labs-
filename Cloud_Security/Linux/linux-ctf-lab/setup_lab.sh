#!/usr/bin/env bash
# ============================================================
#  Linux Fundamentals CTF Lab — Setup Script
#
#  Creates a 10-level, hands-on CTF that teaches core Linux
#  commands: cd, ls, cat, find, grep, chmod, tar, base64,
#  strings, symlinks, wildcards and environment variables.
#
#  Usage:
#     bash setup_lab.sh
#     (creates ~/linux-ctf with all the levels)
# ============================================================

set -u

LAB_DIR="$HOME/linux-ctf"

if [ -d "$LAB_DIR" ]; then
    BACKUP="${LAB_DIR}-backup-$(date +%s)"
    echo "[!] $LAB_DIR already exists."
    echo "    Moving it to $BACKUP"
    mv "$LAB_DIR" "$BACKUP"
fi

mkdir -p "$LAB_DIR"
cd "$LAB_DIR" || { echo "[x] Failed to cd into $LAB_DIR"; exit 1; }

echo "[*] Building Linux CTF lab in $LAB_DIR"

# ---------- Root files ----------
cat > start.txt <<'EOF'
============================================================
  WELCOME TO THE LINUX FUNDAMENTALS CTF LAB
============================================================

Your mission: find the flag (CTF{...}) in each level directory,
from level1 to level10, and write it into flags.txt.

Rule: type the commands yourself. Look things up with:
     man COMMAND      (manual)
     COMMAND --help   (quick help)
     help             (bash built-ins)

The flags get harder as you go. Good luck, and happy hacking!
============================================================
EOF

cat > flags.txt <<'EOF'
# Fill in each flag as you find it.

Level 1  :
Level 2  :
Level 3  :
Level 4  :
Level 5  :
Level 6  :
Level 7  :
Level 8  :
Level 9  :
Level 10 :
EOF

# ---------- Level 1 : ls, cd, cat ----------
mkdir -p level1
cat > level1/note1.txt <<'EOF'
Nothing here. Try the other notes.
EOF
cat > level1/note2.txt <<'EOF'
Still nothing. The flag is in one of these notes.
EOF
cat > level1/note3.txt <<'EOF'
Well done! CTF{cat_is_your_friend}
EOF
cat > level1/note4.txt <<'EOF'
Keep looking. Maybe read them all.
EOF

# ---------- Level 2 : hidden files ----------
mkdir -p level2
cat > level2/readme.txt <<'EOF'
The flag is in a hidden file in this directory.
Hidden files start with a dot ( . ).

  ls -la     -> lists ALL files, including hidden ones
  cat .file  -> reads a hidden file
EOF
cat > level2/.secret <<'EOF'
CTF{hidden_things_hide}
EOF

# ---------- Level 3 : find ----------
mkdir -p level3/a/b/c/d
cat > level3/note.txt <<'EOF'
The flag is buried somewhere in this directory tree.
The find command searches recursively for files:

  find . -type f -name "*.txt"
EOF
cat > level3/a/b/c/d/flag.txt <<'EOF'
You found me deep in the tree! CTF{find_me_everywhere}
EOF

# ---------- Level 4 : grep ----------
mkdir -p level4
{
    for i in $(seq 1 200); do
        echo "INFO request#$RANDOM completed"
    done
    echo "WARNING possible flag detected: CTF{grep_is_magic}"
    for i in $(seq 1 200); do
        echo "INFO request#$RANDOM completed"
    done
} > level4/log.txt
cat > level4/note.txt <<'EOF'
The flag is hidden in ONE line of this large log file.
Do NOT read the whole file. Search inside it:

  grep "CTF" log.txt

grep searches for text within files (case: -i, lines: -n).
EOF

# ---------- Level 5 : permissions ----------
mkdir -p level5
echo "just a normal text file" > level5/normal.txt
cat > level5/run.sh <<'EOF'
#!/bin/bash
echo "CTF{permissions_matter}"
EOF
chmod 755 level5/run.sh
cat > level5/note.txt <<'EOF'
The flag is hidden in a file with EXECUTE permission.

  ls -l                          -> see permissions (rwx)
  find . -type f -executable     -> find executable files

When you find the script, RUN it:
  ./run.sh
EOF

# ---------- Level 6 : tar archives ----------
mkdir -p level6/.work
echo "CTF{tar_time_archives}" > level6/.work/flag.txt
tar -czf level6/archive.tar.gz -C level6/.work flag.txt
rm -rf level6/.work
cat > level6/note.txt <<'EOF'
The flag is inside a compressed archive.
First, SEE what's inside without extracting:

  tar -tzf archive.tar.gz

Then extract it:
  tar -xzf archive.tar.gz

Then read the flag file you extracted.
EOF

# ---------- Level 7 : base64 ----------
mkdir -p level7
echo "CTF{encoding_is_not_encryption}" | base64 > level7/encoded.txt
cat > level7/note.txt <<'EOF'
The flag is ENCODED in base64. Decode it:

  base64 -d encoded.txt
  # or
  cat encoded.txt | base64 -d

Remember: base64 is ENCODING, not encryption — anyone can decode it.
EOF

# ---------- Level 8 : strings on a binary ----------
mkdir -p level8
{
    head -c 64 /dev/urandom
    printf 'CTF{strings_reveal_all}'
    head -c 64 /dev/urandom
} > level8/binary
cat > level8/note.txt <<'EOF'
The flag is inside this binary file, surrounded by random junk.
If you cat it you'll get garbage. Instead, extract readable text:

  strings binary | grep CTF

The strings command pulls readable text out of binary files.
EOF

# ---------- Level 9 : symlinks ----------
mkdir -p level9/target
echo "CTF{symlinks_point_the_way}" > level9/target/real_flag.txt
ln -s target/real_flag.txt level9/flag_link
cat > level9/note.txt <<'EOF'
There is a symlink (shortcut) in this directory:  flag_link

  ls -la              -> shows the link and where it points
  cat flag_link       -> reads through the link
  readlink flag_link  -> shows the target path
EOF

# ---------- Level 10 : wildcards + environment ----------
mkdir -p level10
echo "CTF{you_conquered_linux}" > level10/flag.txt
echo "CTF{you_conquered_linux}" > level10/fake_flag.bin
cat > level10/note.txt <<'EOF'
Final level! Two skills to test:

1) WILDCARDS - match multiple files at once:
     ls *.txt
     cat *flag*.txt

2) ENVIRONMENT - inspect your shell:
     echo $USER
     echo $HOME
     printenv | head
     env

Grab the flag, write it into ../flags.txt, and you are DONE!
EOF

# ---------- Done ----------
echo ""
echo "============================================================"
echo "  Lab ready!"
echo "  Start:   cat ~/linux-ctf/start.txt"
echo "  Begin:   cd ~/linux-ctf/level1 && ls"
echo ""
echo "  Stuck?       See README.md (hints per level)"
echo "  Finished?    Compare with SOLUTIONS.md"
echo "============================================================"
