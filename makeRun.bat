@echo off
cd  %~dp0
rd /S/Q .\build
rd /S/Q .\dist

pyinstaller -i .\source\images\common\psybuilder.ico -w --noconfirm --k=asdgaFgWE1e42a --hidden-import pkg_resources.py2_warn run.py
rem mac ox: pyinstaller -i ./source/images/common/psybuilder.ico -w --noconfirm --k=asdgaFgWE1e42a --hidden-import pkg_resources.py2_warn run.py

echo on

pause
