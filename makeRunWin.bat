@echo off
cd  %~dp0
rd /S/Q .\build
rd /S/Q .\dist

pyinstaller -i .\source\images\common\psybuilder.ico -w --clean --add-data source;source --add-data yanglabMFuns;yanglabMFuns --noconfirm --k=asdgaFgWE1e42a --hidden-import pkg_resources.py2_warn psyBuilder.py
rem # mac ox: pyinstaller -i ./source/images/common/psybuilder.ico -w --noconfirm --k=asdgaFgWE1e42a --hidden-import pkg_resources.py2_warn psyBuilder.py


cd "C:\Program Files (x86)\Inno Setup 6\"

.\Compil32 /cc "C:\Users\Administrator\PycharmProjects\ptbGui\psyBuilder.iss"

cd  %~dp0
makecab ../psyBuilder.exe ../psyBuilder%date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2%Win.zip

rd /S/Q .\build
echo on

pause
