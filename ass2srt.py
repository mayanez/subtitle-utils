
'''
Converts 1 simple (i.e. single sub) .ass file to a .srt file
'''
import codecs
import re
import Tkinter, tkFileDialog


def ass2srt(srcFilepath, dstFilepath, isUTF16):
    if isUTF16:
        f = codecs.open(srcFilepath, "r", "utf-16")
        dst = codecs.open(dstFilepath, 'w', "utf-16")
    else:
        f = codecs.open(srcFilepath, "r")
        dst = open(dstFilepath, 'w')

    # Count of how many subtitles. Written to dst before each subtitle.
    count = 0 
 
    for line in f:

        toks = line.split()

        if len(toks) == 0:
            continue
    
        # .srt files have no styling. Only dialogue and timing.
        if(toks[0] == "Dialogue:"):
            formats = toks[1].split(',,')
            times = formats[0].split(',')
            text = formats[-1];
            start = times[1]
            end = times[2];

            text = re.sub('\N', '\r\n', text)
            count += 1

            dst.write(str(count) + "\n")
            dst.write(start + " --> " + end + "\n")
            dst.write(text + "\n\n")
            
if __name__ == '__main__':

    # define options for opening a file
    fileopts = {}
    fileopts['filetypes'] = [('ass files', '.ass')]
    fileopts['title'] = 'Choose .ass file to convert'
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


    ass2srt(srcFilepath, dstFilepath, isUTF16=True);

