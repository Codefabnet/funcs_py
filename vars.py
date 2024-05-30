import os
import sys
import subprocess
import fparse

subcall = fparse.subcall
getfuncs = fparse.getfuncs
finduse = fparse.finduse
listref = fparse.listref

inval = sys.argv[1:2]
#inval = sys.argv[1]


ctype = 0
htype = 4
stype = 8
diagsonly = 2
nodiags = 3
depth = 0
stack =[]




#if len(sys.argv) > 2:
#    inop = int(sys.argv[2:][0])
#else:    
inop = nodiags
#print inop
func = inval[0]
sfile = '%'
sfunc = '%'
sline = '0'

def print_debug():
     print()
#     print
#     print "depth = " , depth
#     print "func = "  , func
#     print "sfunc = " , sfunc
#     print "sel = "   , sel
#     print "stack:"
#     for x in stack[:]:
#         print x
     idx = 0
     for idx in range(len(stack)):
         print (" " * idx * 2, stack[len(stack)-idx-1][2])
         print (" " * idx * 2, "  |") 
     print (" " * idx * 2, " ", func)


if len(sys.argv) == 2:

    # find where the function is referenced in the source tree
    func_ref_list = finduse(func, inop)

    # print and indexed list of references
    listref(func_ref_list, func, ctype)

    # user selects a reference location
    inp = input('> ')
#    print inp[0]
#    print inp[1:]
    while len(inp) != 0 and \
           (inp.isdigit() or \
            inp[0] == 'U'  or \
            inp[0] == 'D'  or \
            inp[0] == 'd'  or \
            inp[0] == 'h'  or \
            inp[0] == 'c'  or \
            inp[0] == 'f'  or \
            inp[0] == 't'  or \
            inp[0] == 'g'  or \
            inp[0] == 's'):

        if inp.isdigit():
            # open file at reference location
            sfile = func_ref_list[int(inp)][0]
            sline = func_ref_list[int(inp)][1]
            sfunc = func_ref_list[int(inp)][3]
            sel = [sfile, sline, sfunc]
            os.system('gvim ' + sfile + ' +' + sline)
            print_debug()

        if inp[0] == 'd' and sfile != '%' and depth > 0:
            depth -= 1
            sel = stack[depth-1]
            stack.pop()
            print_debug()
            sfile = sel[0]
            sline = sel[1]
            sfunc = sel[2]
            if depth > 0:
                func_ref_list = finduse(sfunc, inop)
                listref(func_ref_list, sfunc, ctype)
            else:
                func_ref_list = finduse(func, inop)
                listref(func_ref_list, func, ctype)

        if inp[0] == 'F':
            print (inp[1:])
#            sfile = func_ref_list[int(inp[1:])][0]
#            sline = func_ref_list[int(inp[1:])][1]
#            sfunc = func_ref_list[int(inp[1:])][3]
#            sel = [sfile, sline, sfunc]
#            func_ref_list = finduse(sfunc, inop)
#            listref(func_ref_list, sfunc, ctype)
#            stack.append([sfile, sline, sfunc])
#            depth += 1
            print_debug()


        if inp[0] == 'U':
            sfile = func_ref_list[int(inp[1:])][0]
            sline = func_ref_list[int(inp[1:])][1]
            sfunc = func_ref_list[int(inp[1:])][3]
            sel = [sfile, sline, sfunc]
            func_ref_list = finduse(sfunc, inop)
            listref(func_ref_list, sfunc, ctype)
            stack.append([sfile, sline, sfunc])
            depth += 1
            print_debug()

        if inp[0] == 'u' and sfile != '%':
            func_ref_list = finduse(sfunc, inop)
            listref(func_ref_list, sfunc, ctype)
            stack.append([sfile, sline, sfunc])
            depth += 1
            print_debug()

        if inp[0] == 't' and sfile != '%':
            tempdir = os.environ['TEMP']
            ffile = open(tempdir + '\\functemp', 'w')
            ffile.write(":split " + sfile + ' | :' + sline)
            ffile.close()
            break
        if inp[0] == 'h':
            # find where the function is referenced in the source tree
            func_ref_list = finduse(func, htype)
            print (len(func_ref_list))
            # print and indexed list of references
            listref(func_ref_list, func, htype)

        if inp[0] == 'c':
            # find where the function is referenced in the source tree
            func_ref_list = finduse(func, ctype)
            print (len(func_ref_list))
            # print and indexed list of references
            listref(func_ref_list, func, ctype)

        if inp[0] == 's':
            # find where the function is referenced in the source tree
            func_ref_list = finduse(func, stype)
            print (len(func_ref_list))
            # print and indexed list of references
            listref(func_ref_list, func, ctype)

        if inp[0] == 'g':
            # find where the function is referenced in the source tree
            func_ref_list = finduse(func, diagsonly)
            print (len(func_ref_list))
            # print and indexed list of references
            listref(func_ref_list, func, ctype)

        print()
        print()
        # user selects a reference location
        inp = input('> ')

#    print depth
    stack.reverse()
    for x in stack[:]:
        print (x[2])
    print (func)




