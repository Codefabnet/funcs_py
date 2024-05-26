REM @FOR /F "eol=; tokens=1,2,3* delims=: " %%i in ('g %1') do @echo :split %%i ^| :%%j
c:\dev\scripts\vars.py %1
