@echo off
@REM UTF-8
chcp 65001

set DATETIMEFILEPATH=..\app\base\build_datetime.py

echo # Build Date time > %DATETIMEFILEPATH%
echo # This file is automatically generated by build/write_build_datetime.bat >> %DATETIMEFILEPATH%
echo. >> %DATETIMEFILEPATH%
echo BUILD_DATE='%date%' >> %DATETIMEFILEPATH%
echo BUILD_TIME='%time%' >> %DATETIMEFILEPATH%
echo. >> %DATETIMEFILEPATH%