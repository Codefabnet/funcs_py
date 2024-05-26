import os
import json
import sys
from fparse import getfuncs

#getfuncs = fparse.getfuncs


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
                    print src_filename, "is not a file!"
                if len(src_filename) > 0:
                    print src_filename
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


