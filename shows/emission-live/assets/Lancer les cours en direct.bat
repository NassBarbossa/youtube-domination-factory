@echo off
title Convergence - cours en direct
cd /d "%~dp0obs"
set PYTHONIOENCODING=utf-8
python cours_live.py
pause
