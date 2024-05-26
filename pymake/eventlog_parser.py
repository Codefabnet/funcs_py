
elog_file = open("eventlog.txt", "r")
for log_line in elog_file:
    if "ailure" in log_line and "DSPTCH" in log_line:
#        print log_line
        log_line = log_line[log_line.find("DSPTCH"):]
        if not "0139" in log_line[8:12]:
            print log_line
elog_file.close
