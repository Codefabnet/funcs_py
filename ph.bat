@echo off
echo %1 | ctags -n --fields=+nzK-s --c-kinds=+p --filter=yes | grep kind:prototype | cut -f 1 -d ;
