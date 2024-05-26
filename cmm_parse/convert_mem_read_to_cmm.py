#!/c/Python26/python
import os
import sys


class mem_dump_convertor:

    def find_data(self, line_input):
        line = line_input.readline()
        while line:
            if "---------------------------------------------" in line:
                    break
            line = line_input.readline()


    def find_entry(self, line_input, entry):
        line = line_input.readline()
        while line:
            if "Entry" in line:
                hwords = line.split(" ")
                if (int(hwords[1]) == entry):
                    addr_str = hwords[7][2:10]
                    self.addr_int = int(addr_str, 16)
                    self.find_data(line_input)
                    break
            line = line_input.readline()


    def convert_to_cmm(self, filein, entry):

        try:
            finput = open(filein,"r")
        except Exception, exc:
                print "Unable to open file %s" % (filein)
        self.find_entry(finput, entry)
        line = finput.readline()
        while line:
            fields = line.split("|") 
            if len(fields) >= 3:
                sys.stdout.write("Data.set ")
                sys.stdout.write("0x")
                sys.stdout.write(hex(self.addr_int))
                self.addr_int += 16
                words = fields[1].split(" ")
                for word_index in range(1, 17):
                    if words[word_index] == "--":
                        break
                    sys.stdout.write(",0x")
                    sys.stdout.write(words[word_index])
                sys.stdout.write("\n")
            else:
                break
            line = finput.readline()
        finput.close()

        sys.exit(0)
    


def Main():

    convertor = mem_dump_convertor()
    if len(sys.argv) > 2:
        entry = int(sys.argv[2:][0])
    else:
        entry = 0
    return convertor.convert_to_cmm(sys.argv[1], entry)

if __name__ == "__main__":
    sys.exit(Main())
