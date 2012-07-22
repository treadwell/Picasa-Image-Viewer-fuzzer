# A fuzzer for Picasa Image Viewer.  Fuzzer works on images of various types
# placed in an \images\ subdirectory.  It picks an image at random, corrupts
# the file and then uses Picasa Image Viewer to attempt to open the file.

import math
import random
import string
import subprocess
import time
import os

#################### configuration ####################

location = "C:\Python27\CS258 Software Testing\images\/"

apps = ["C:\Program Files (x86)\Google\Picasa3\PicasaPhotoViewer.exe"]

fuzz_output = ""

FuzzFactor = 250
num_tests = 1000
num_crashed = 0

print "start"

#################### end configuration ####################

start_time = time.time()

#################### start Charlie Miller code ####################

for i in range(num_tests):
    print "test", i
    file_choice = random.choice([x for x in os.listdir(location) if os.path.isfile(os.path.join(location, x))])
    extension = file_choice.split(".")[-1]
    fuzz_output = "fuzz." + extension
    app = random.choice(apps)
    buf = bytearray(open(location+file_choice, 'rb').read())
    
    numwrites = random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)

#################### end Charlier Miller code ####################

    open(fuzz_output, 'wb').write(buf)
    process = subprocess.Popen([app, fuzz_output])

    time.sleep(1)
    crashed = process.poll()
    if crashed:
        num_crashed += 1
        print "Number of crashes is", num_crashed
        print "number of writes:", numwrites
        print "return code:", process.returncode
        print
    else:
        process.terminate()
end_time = (time.time() - start_time)
print "Number of crashes is", num_crashed
print "Time taken to complete %d iterations is %f s" % (num_tests, end_time)
