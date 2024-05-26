@echo off
echo %1 | ctags -nu --fields=+nzK-s --filter=yes | grep "kind:function\|kind:macro" | cut -f 1 -d ;
