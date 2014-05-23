'''
This will edit the timing of a .srt file by the user-set variables below.
'''

import codecs
import re
import math
import Tkinter, tkFileDialog


###################### USER VARIABLES ##################
# Change variables as needed.

# Time to change by.
# Positive to add time. Negative to subtract time.
hourChange = 0
minuteChange = 0
secondChange = 0
millisecondChange = 0
########################################################



delta = (hourChange * 60 * 60 * 1000) + (minuteChange *  60 * 1000) + (secondChange * 1000) + millisecondChange


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def toMilli(timeFields):
    milli = 0
    milli += int(timeFields[0]) * 60 * 60 * 1000
    milli += int(timeFields[1]) * 60 * 1000
    milli += int(timeFields[2]) * 1000
    milli += int(timeFields[3])
    
    return milli

def toTime(milli):
    
    time = ""
    
    hour_frac = (milli / float(60 * 60 * 1000) )
    (hour_deci, hour) = math.modf(hour_frac)
    time += str( int(hour) ).zfill(2) + ":"
    
    min_frac = hour_deci * 60
    (min_deci, minute) = math.modf(min_frac)
    time += str( int(minute) ).zfill(2) + ":"
    
    sec_frac = min_deci * 60
    (sec_deci, sec) = math.modf(sec_frac)
    time += str( int(sec) ).zfill(2) + ","
    
    milli_sec= int(sec_deci * 1000)
    time += str( int(milli_sec) ).zfill(3)
    
    return time
    
def editTime(start, end, delta):
    sFields = re.findall(r"[0-9]+", start)
    eFields = re.findall(r"[0-9]+", end)
    
    sMilli = toMilli(sFields)
    eMilli = toMilli(eFields)
    
    new_sMilli = sMilli + delta
    new_eMilli = eMilli + delta
    
    new_start = toTime(new_sMilli)
    new_end = toTime(new_eMilli)
    
    return (new_start, new_end)

if __name__ == '__main__':

    # define options for opening a file
    fileopts = {}
    fileopts['filetypes'] = [('srt files', '.srt')]
    fileopts['title'] = 'Choose .srt file to edit'
    # defining options for saving dst file
    dstopts = {}
    dstopts['title'] = 'Choose filename for .srt file'
    dstopts['filetypes'] = [('srt files', '.srt')]
    dstopts['defaultextension'] = '.srt'
    dstopts['initialfile'] = 'output.srt'


    root = Tkinter.Tk()
    root.withdraw()
    srcFilepath = tkFileDialog.askopenfilename(**fileopts)
    
    dstFilepath = tkFileDialog.asksaveasfilename(**dstopts)

    srcFile = codecs.open(srcFilepath, "r")
    dstFile = codecs.open(dstFilepath, "w")

    timeIsNextLine = False

    for line in srcFile:
        if timeIsNextLine:
            fields = line.split(" ") # ["01:37:48,140", "-->", "01:37:49,620"]
            start = fields[0]    # "01:37:48,140"
            end = fields[2]      # "01:37:49,620"
            
            (new_start, new_end) = editTime(start, end, delta)
            dstFile.write(new_start + " --> " + new_end + "\n")
            timeIsNextLine = False
        else:
            dstFile.write(line)
        
        if is_number(line):
            timeIsNextLine = True
    
    