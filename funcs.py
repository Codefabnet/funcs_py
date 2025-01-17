import os
import sys
import subprocess
import fparse

getfuncs = fparse.getfuncs
findcalls = fparse.findcalls
finduse = fparse.finduse
listref = fparse.listref

inval = sys.argv[1:2]
#print (inval)
sort = 1
line = 0

# The second arg is either a line number or sort option
if len(sys.argv) > 2:
    sort = int(sys.argv[2:][0])

# Anything greater than 1 is a line number to match in a function
if sort > 1:
    line = sort
    sort = 0

#print (sort)
#print (line)

ctype = 0
htype = 4
stype = 8
diagsonly = 2
nodiags = 3

#tempdir = os.environ['TEMP']
#print (tempdir + '\\functemp')

#ffile = open(tempdir + '\\functemp', 'w')
#ffile.write("smoething")
#ffile.close()

func = ""

# get a list of functions in a given file and print (an indexed list)
func_desc_list = getfuncs(inval[0], 0, sort)
for x in range(len(func_desc_list)):
    if line > 0:
        if line < int(func_desc_list[x][2]):
            func = func_desc_list[x-1][0]
            print (func) #func_desc_list[x-1][0]
            sel = input('> ')
            break
    else:
        print (str(x) + ':', '\t', func_desc_list[x][1].decode('UTF-8'), ' - ', func_desc_list[x][2].decode('UTF-8'), '\t', func_desc_list[x][0].decode('UTF-8') )
sfile = '%'
sline = '0'

# user selects a fucntion from the file
if line == 0:
    sel = input('> ')
while sel.isdigit() or sel != "":
    if func == "":
        func = func_desc_list[int(sel)][0].decode('UTF-8')

    # find where the function is referenced in the source tree
    func_ref_list = finduse(func, ctype)

    # print (and indexed list of references)
    listref(func_ref_list, func, ctype)

    # user selects a reference location
    sel = input('> ')
    while sel.isdigit() or sel == 'h' or sel == 'c' or sel == 'f' or sel == 's' or sel == 't':

        if sel.isdigit():
#            print (func)
#            findcalls(func)
            # open file at reference location
            os.system('gvim ' + func_ref_list[int(sel)][0] + ' +' + func_ref_list[int(sel)][1])
            sfile = func_ref_list[int(sel)][0]
            sline = func_ref_list[int(sel)][1]
        if sel == 't':
            tempdir = os.environ['TEMP']
            ffile = open(tempdir + '\\functemp', 'w')
            ffile.write(":split " + sfile + ' | :' + sline)
            ffile.close()
            break
        if sel == 'h':
            # find where the function is referenced in the source tree
            func_ref_list = finduse(func, htype)
            print (len(func_ref_list))
            # print (and indexed list of references)
            listref(func_ref_list, func, htype)

        if sel == 'c':
            # find where the function is referenced in the source tree
            func_ref_list = finduse(func, ctype)
            print (len(func_ref_list))
            # print (and indexed list of references)
            listref(func_ref_list, func, ctype)

        if sel == 's':
            # find where the function is referenced in the source tree
            func_ref_list = finduse(func, stype)
            print (len(func_ref_list))
            # print (and indexed list of references)
            listref(func_ref_list, func, ctype)
 
        if sel == 'f':
            print ('index', '\t', 'line', '\t',  'function' )
            for x in range(len(func_desc_list)):
                print (str(x) + ':', '\t', func_desc_list[x][2].decode('UTF-8'), '\t', func_desc_list[x][0].decode('UTF-8') )
            sel = input('> ')
            break

        # user selects a reference location
        sel = input('> ')




