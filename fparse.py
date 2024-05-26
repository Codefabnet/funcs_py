import subprocess
import json
import os
import fnmatch
#from makefile_parser import makefile_parser


#mparser = makefile_parser

ctype = 0
htype = 4
stype = 8
diags = 2
nodiags = 3

class makefile_parser:

    dir_defs = {"SOFTWARE_DIR":"."}                    
    files_func_dir = {} 
    func_list = list()

    def find_definition_in_makefile(self, make_file, find_key):

        # scsn each line of the makefile
        make_file.seek(0,0)
        make_line = make_file.readline()
        while make_line:

            # look for the current dir reference
            if find_key == make_line[:len(find_key)]:

                # add the definition as a value for the top level dir reference
                val = make_line.split()[-1:][0]

                if "$" in val:
                    new_key = val.split(")")[:1][0][2:]
                    if new_key in self.dir_defs and self.dir_defs[new_key] != "" and not "$" in self.dir_defs[new_key]:
                        new_val = val.replace('$(' + new_key + ')', self.dir_defs[new_key])
                    else:
                        new_val = self.find_definition_in_makefile(make_file, new_key)
                        new_val = val.replace('$(' + new_key + ')', new_val)
                    val = new_val
                break

            make_line = make_file.readline()
        return val

    def parsemake(self, make_file):

        make_line = make_file.readline()
        while make_line:
            if "CORE1_SRC_FILES" in make_line[:15] or "CORE0_SRC_FILES" in make_line[:15]:
                src_filename = make_line.split()[-1:][0]

                # Get the $() directory reference at the beginning of the src file
                new_key = src_filename.split(")")[:1][0][2:]
                make_file_pos = make_file.tell()
                new_val = self.find_definition_in_makefile(make_file, new_key)
                make_file.seek(make_file_pos, 0)
                src_filename = src_filename.replace('$(' + new_key + ')', new_val)
                if not os.path.isfile(src_filename):
                    print (src_filename, "is not a file!")
                if len(src_filename) > 0:
                    print (src_filename)
                    self.files_func_dir[src_filename] = getfuncs(src_filename, 0, 0) 
                
            make_line = make_file.readline()



    def get_files_func_dir(self):

        if len(self.files_func_dir) == 0:
            # build a directory of functions with filename keys.
            if os.path.exists("files_func_dir.json"):
                with open("files_func_dir.json", "r") as json_obj_file: 
                    self.files_func_dir = json.load(json_obj_file)
            else:
                with open("build\\scripts\\monet.mak", "r") as make_file: 
                    self.parsemake(make_file)

                with open("files_func_dir.json", "w") as json_obj_file: 
                    json.dump(self.files_func_dir, json_obj_file)

        return self.files_func_dir


    def get_func_list(self):

        if len(self.func_list) == 0:
            # build a list of all functions with filename and line number.
            if os.path.exists("func_list.json"):
                with open("func_list.json", "r") as json_obj_file:
                    self.func_list = json.load(json_obj_file)
            else:
                file_list = self.get_files_func_dir().keys()
                for file_name in file_list:
                    [self.func_list.append(func_name) for func_name in self.files_func_dir[file_name]]
                with open("func_list.json", "w") as json_obj_file:
                    json.dump(self.func_list, json_obj_file)
        return self.func_list


mparser = makefile_parser()


def subcall(fcall, fpar):
    "function to call subprocess Popen"

#    print 'fparse.py, subcall', fcall, fpar
    p = subprocess.Popen([fcall,  fpar], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    lines_out = out.splitlines()
    return lines_out


def get_end_of_func(func_desc_list, ffile):
    for x in range(len(func_desc_list)):
        src_file = open(ffile, "r")
        count = 0
        found_line = 0

        # goto the line that ctag says the function starts
        while count < int(func_desc_list[x][2]):
            src_line = src_file.readline()
            count += 1

        if x < len(func_desc_list)-1:
            # if not the last function in the list, stop looking for end at the next function in the list
            while count < int(func_desc_list[x+1][2]):
                src_line = src_file.readline()
                count += 1
                if '}' in src_line:
                    found_line = count
            if found_line > 0:
                # the last '}' is the end of function
                func_desc_list[x].append(found_line)
            else:
                # could not find a '}' (macro?), use next function in list minus 1 as end of function
                func_desc_list[x].append(int(func_desc_list[x+1][2])-1)
        else:
            # last function in the list, look for the last '}'
            while src_line:
                if '}' in src_line:
                    found_line = count
                src_line = src_file.readline()
                count += 1
            func_desc_list[x].append(found_line)

    return func_desc_list


def getfuncs(ffile, fprint, sort):
    "get list of functions in file"
    if os.path.exists("files_func_dir.json"):
        with open("files_func_dir.json", "r") as json_obj_file: 
            files_func_dir = json.load(json_obj_file)
        func_desc_list = files_func_dir[ffile] 
    else:
        func_tags_list = subcall('pu.bat',  ffile)
        func_desc_list = [func_tags_list[x].split() for x in range(len(func_tags_list))]
        func_desc_list = get_end_of_func(func_desc_list, ffile)

    if sort == 1:
        func_desc_list.sort()
    if fprint == 1:
        print ('index', '\t', 'line', '\t',  'function' )
        for x in range(len(func_desc_list)):
            print (str(x) + ':', '\t', func_desc_list[x][2], ' - ', func_desc_list[x][3], '\t', func_desc_list[x][0] )
    return func_desc_list

def findcalls(func):

    func_list = mparser.get_func_list()
    for func_desc in func_list:
        if func == func_desc[0]:

            print (func, func_desc)
            ffile = open(func_desc[1], "r")
            count = 0
            while count < int(func_desc[2]):
                ffile.readline()
                count += 1

            src_line = ffile.readline().strip()
            while src_line and count < int(func_desc[3]):


                print ("\n------------", src_line)
                if "//" in src_line:
                    src_line = src_line.split("//")[:-1][0] 
#                    print ("removed '//'\n", src_line)

                if len(src_line) == 0:
#                    print ("skip")
                    count += 1
                    continue

                while src_line.rfind(";") == -1:
                    src_line += ffile.readline().strip()
                    count += 1
                    if count >= int(func_desc[3]):
                        src_line = src_line[:src_line.rfind("}")+1]
                        break
                print (src_line)








                if "(" in src_line:
                    calls = src_line.split("(")[:-1] 

                    excludes = ["if", "sizeof", "while", "ASSERT", "for", "switch"]
                    caller_list = [x.strip() for x in calls if not x.isspace()]
#                    if len(caller_list) != 0:
#                        caller = caller_list[0]
                    print (caller_list, "\n", calls)
                    for caller in caller_list:
#                    caller = [x for x in calls if not x.isspace()]
#                        if "if" in caller or "sizeof" in caller or "while" in caller or caller.isspace():
                        if caller.isspace() or caller[-1:] == "=" or caller[-1:] == "," or caller[-1:] == "~":
                            caller_list.remove(caller)
                        print (caller)
                        for exclude in excludes:
                            if exclude in caller:
                                caller_list.remove(caller)

                    for caller in caller_list:
                        print (count+1, len(caller), caller)

                count += 1
                src_line = ffile.readline().strip()

            ffile.close()












def finduse(func_name, flags):
    "Get all references to a symbol"
#    print 'fparse.py, finduse', func_name
    if (flags & stype) == stype:
        grepopt = ' -IRnw --include=*.s --include=*.S '
        filepat = ' ./*'
    elif (flags & htype) == htype:
        grepopt = ' -IRnw --include=*.h '
        filepat = ' ./*'
    elif flags == ctype:
        grepopt = ' -IRnw --include=*.c '
        filepat = ' ./*'
    elif (flags & nodiags) == nodiags:
        grepopt = ' -IRnw --include=*.c --exclude-dir=diags '
        filepat = ' ./*'
    elif (flags & nodiags) == diags:
        grepopt = ' -IRnw --include=*.c '
        filepat = ' ./diags\\cpu_1\\*'
    func_grep_list = subcall('grep', [grepopt + func_name + filepat])
    func_ref_list=[func_grep_list[x].split(':') for x in range(len(func_grep_list))]

    for func_ref in func_ref_list[:]:
#        print 'fparse.py, finduse', func_ref
        # remove commented out code
        if '//' in func_ref[2]:
            if func_ref[2].find('//') < func_ref[2].find(func_name):
                func_ref_list.remove(func_ref)
                continue
        if (flags & htype) == htype:
            func_grep_list = subcall('ph.bat',  func_ref[0])
            func_href_list=[func_grep_list[i].split() for i in range(len(func_grep_list))]
            for func_href in func_href_list[:]:
                if func_name == func_href[0] and func_ref[1] == func_href[2]:
                    func_ref_list.remove(func_ref)
                    break
                
    return func_ref_list

def listref(func_ref_list, func_name, ftype):
    "print the list of references and the function containing each"
#    print "listref"
    func = ""
    if ftype == 4: # htype
        func = func_name
    for x in range(len(func_ref_list)):
#        print 'func_ref_list[x] =', func_ref_list[x][0], '\t', func_ref_list[x][1], '\t', func_ref_list[x][2]
        func_desc_list = getfuncs(func_ref_list[x][0], ftype, 1)
        func_desc_list.sort(key=lambda line: int(line[2]))
        func_ref_list[x].append(func)

        # find the function where the reference is made
        for y in range(len(func_desc_list)):
#            print 'func_desc_list[y] =', func_desc_list[y][0], '\t', func_desc_list[y][1], '\t', func_desc_list[y][2]
            if int(func_ref_list[x][1]) >= int(func_desc_list[y][2]):
                    func_ref_list[x][3] = func_desc_list[y][0]
#                    func = func_desc_list[y][0]
        # is this where the function defined?                     
        if ftype == 0:  # ctype
#            if func == func_name: 
            if func_ref_list[x][3] == func_name: 
                print ('\ndefined here:' )
                print (str(x) + ':', func_ref_list[x][1], func_ref_list[x][0], '\t', func_ref_list[x][2].strip(), '\n' )
            else:
#                print str(x) + ':', 'called in', func_ref_list[x][0], ': line', func_ref_list[x][1], ':', func+'()', 'function:'
                print (str(x) + ':', 'called in', func_ref_list[x][0], ': line', func_ref_list[x][1], ':', func_ref_list[x][3]+'()', 'function:')
                print ('\t', func_ref_list[x][2].strip(), '\n')
#                func_ref_list[x].append(func)
        else:
            print ((str(x) + ':', 'ref in header file,', func_ref_list[x][0], ': line', func_ref_list[x][1]))
            print ('\t', func_ref_list[x][2].strip(), '\n')


def findinsym(refobj):

    mfiles = []
    Ret = []

    for root, dnames, fnames in os.walk('build'):
        for fname in fnmatch.filter(fnames, '*.sym'):
            mfiles.append(os.path.join(root, fname))

    for file_name in mfiles[:]:
        ref_grep_list = subcall('grep', [' -w ' + refobj + ' ' + file_name])
        if len(ref_grep_list) > 0:
            Ret.append([ ref_grep_list[0], file_name])

    return Ret
