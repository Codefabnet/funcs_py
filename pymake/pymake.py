import subprocess
import os
import fnmatch
import sys


ctype = 0
htype = 4
stype = 8
diags = 2
nodiags = 3

class pymake:

    def subcall(self, fpar):
        "function to call subprocess Popen"

        p = subprocess.Popen(fpar, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.err_lines = err.splitlines()
        self.out_lines=out.splitlines()
        return p.returncode

    def do_fwcopy(self):

        for line in self.out_lines:
            if "fwcopy" in line:
                line = line[line.find("fwcopy"):]
                subprocess.call(line, shell=True)


    def do_make(self, make_args):

        make_args.insert(0, "make")
        mk_retcode = self.subcall(make_args)
        if (mk_retcode !=0) and ("data_structs" in self.err_lines[0]):
            mk_retcode = self.subcall(make_args)
        if (mk_retcode == 0):
            print "Success"
            self.do_fwcopy()
        else:
            for line in self.out_lines:
                print line
            for line in self.err_lines:
                print line

def Main():

    maker = pymake()

    print sys.argv
    maker.do_make(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(Main())

