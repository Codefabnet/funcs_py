#!/bin/bash

echo $1 | ctags-exuberant -nu --fields=+nzK-s --filter=yes | grep "kind:function\|kind:macro" | cut -f 1 -d ';'
#ctags
