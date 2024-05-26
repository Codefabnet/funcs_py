@echo off
doskey funcs=FOR /F "usebackq tokens=1,2,3*" %i IN  (`c:\dev\scripts\parse_ctags.bat $1`) do @echo %k %i
doskey svndiff=svn diff $1 --diff-cmd c:\dev\scripts\diffcmd.bat
doskey diffcmd=gvim -d $6 $7
doskey xgrp=grep -IRn --exclude=*.txt --exclude=*.map --exclude=*.tdd --exclude=*.bin --exclude-dir=.svn $1 *
doskey igrp=grep -IRn --include=*.c --include=*.h $1 *
doskey find=C:\MinGW\msys\1.0\bin\find
doskey /macros
