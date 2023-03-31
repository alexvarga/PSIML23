import subprocess
import sys
strlen = 0

analysis_script = "morse.py"

for i in range(10):
    command = '"%s" "%s" "%s"' % (sys.executable,      # command
                                       analysis_script,     # argv[0]
                                       "..\..\morse_code\case-"+str(i)+".in")             # argv[2]
    subprocess.Popen(command)  # Run script and pass it the files.

    print(command)
