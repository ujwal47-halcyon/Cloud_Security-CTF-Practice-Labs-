@echo off
echo =======================================================
echo Linux Fundamentals CTF - Flag Submission Portal
echo =======================================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting server...
echo Open http://localhost:5000
echo.
python app.py
pause
