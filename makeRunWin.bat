echo ===================================
echo create modifiedData.py
echo ===================================
set createPsyBuilderDate=%date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2%


rem @echo off
cd  %~dp0

echo CREATED_PSY_DATE = %createPsyBuilderDate% > ./app/modifiedData.py

rd /S/Q .\build
rd /S/Q .\dist


echo ===================================
echo cythonize compile_PTB
echo ===================================
cythonize -i -3 .\app\menubar\compile_PTB.py
rename .\app\menubar\compile_PTB.cp38-win_amd64.pyd compile_PTB.pyd
echo ===================================
echo compile PsyBuilder
echo ===================================

pyinstaller -i .\source\images\common\psybuilder.ico -w --clean --add-data source;source --add-data yanglabMFuns;yanglabMFuns --noconfirm --k=asdgaFgWE1e42a --hidden-import pkg_resources.py2_warn PsyBuilder.py
rem # mac ox: pyinstaller -i ./source/images/common/psybuilder.ico -w --noconfirm --k=asdgaFgWE1e42a --hidden-import pkg_resources.py2_warn psyBuilder.py

echo ===================================
echo create exe file
echo ===================================
cd "C:\Program Files (x86)\Inno Setup 6\"

.\Compil32 /cc "C:\Users\Administrator\PycharmProjects\ptbGui\psyBuilder.iss"

cd  %~dp0
makecab ../PsyBuilder.exe ../PsyBuilder%createPsyBuilderDate%Win.zip

rd /S/Q .\build
rem echo on

pause
