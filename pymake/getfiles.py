import os
import json
import sys
import fparse
#import makefile_parser

getfuncs = fparse.getfuncs
finduse = fparse.finduse
findinsym = fparse.findinsym

mparser = fparse.makefile_parser()

inop = 2 
infile = ""

if len(sys.argv) > 1:
    instr = sys.argv[1:2][0]
    if instr.isdigit():
        inop = int(instr)
    else:
        infile = instr
#    inop = int(sys.argv[1:2][0])

if len(sys.argv) > 2:
    instr = sys.argv[2:3][0]
    if instr.isdigit():
        inop = int(instr)
    else:
        infile = instr



ctype = 0
htype = 4
stype = 8
diagsonly = 2
nodiags = 3



def parsefile(srcfile, count):
#    print 'getfiles.py, parsefile', srcfile
    funcs_in_srcfile = getfuncs(srcfile, 0, 1)
    R = list()
    for func_file_linum in funcs_in_srcfile:
#        print 'getfiles.py, parsefile', z
        func_used_file_linum = finduse(func_file_linum[0], nodiags)
#        print 'getfiles.py, parsefile', len(B)
        if inop > len(func_used_file_linum):
            SymObjs = findinsym(func_file_linum[0])
            for file_linum in func_used_file_linum[:]:
#                print 'getfiles.py, parsefile', y
                if file_linum[0] == srcfile and file_linum[1] == func_file_linum[2]:
                    print count, '\t: ', func_file_linum[0], '\t- ', srcfile, '+'+file_linum[1]
                    R.append(":split " + srcfile + ' | :' + file_linum[1])
                    count = count + 1
#                    if y[2].strip()[-1:] == '{':
#                        print z[0]
                else:
                    print '\tC ', func_file_linum[0], file_linum[0], file_linum[1], file_linum[2]
            func_used_file_linum = finduse(func_file_linum[0], diagsonly)
            for file_linum in func_used_file_linum[:]:
                print '\tD ', file_linum[0], file_linum[1]
            func_used_file_linum = finduse(func_file_linum[0], htype)
            for file_linum in func_used_file_linum[:]:
                print '\tH ', file_linum[0], '+'+file_linum[1], '\t', file_linum[2]
            func_used_file_linum = finduse(func_file_linum[0], stype)
            for file_linum in func_used_file_linum[:]:
                print '\tS ', file_linum[0], file_linum[1], '\t', file_linum[2].strip()
            if len(SymObjs) > 0:
                for file_linum in SymObjs[:]:
                    print '\t', file_linum

    return R


if len(infile) == 0:


    file_list = mparser.get_files_func_dir().keys()
    func_list = mparser.get_func_list()
    print len(func_list), len(file_list)
    for func_name in func_list:
        print func_name

#    for file_names in files_func_dir.keys():
#        print file_names
#        count += len(parsefile(file_names, count))

#    for func_name in func_list:
#        print func_name

else:
    R = parsefile(infile, 0)
    sel = raw_input('> ')
    if sel.isdigit():
        tempdir = os.environ['TEMP']
        ffile = open(tempdir + '\\functemp', 'w')
        ffile.write(R[int(sel)][0])
        ffile.close()
