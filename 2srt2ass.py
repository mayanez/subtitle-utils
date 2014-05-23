'''
Takes 2 srt files and combines them into 1 ass file. 
First srt file is placed at the top of screen, second at bottom.

'''
import codecs
import re
import Tkinter, tkFileDialog


lines_t = None
lines_b = None

def isNumber(str):
    # print("str is %s\n", str)
    try:
        float(str)
        return True
    except ValueError:
        return False

def writetodst(time, text, dst, pos):

#    This block of values does not change.
    layer = "0"
    name = ""
    marginL = "0000"
    marginR = "0000"
    marginV = "0000"
    effect = ""

    time = time.split();
    t_start = time[0]
    t_end = time[2]
    
    t_start = re.sub('[,]', '.', t_start)
    t_end = re.sub('[,]', '.', t_end)

    t_start = t_start[:-1];
    t_end = t_end[:-1];


    
    dst.write("Dialogue: " + layer + "," + t_start + "," + t_end + "," + pos + "," + 
              name + "," + marginL + "," + marginR + "," + marginV + "," + effect + "," + 
              text)

def get_timerank(timeline):
    start = timeline.split()[0]

    timesequence = re.findall(r"[0-9][0-9]+", start)
    timerank = 0
    rate = 60 * 60 * 1000;
    for t in timesequence:
        # print str(t) + '\n'
        timerank += float(t) * rate
        if t == timesequence[-2]:
            rate /= 1000;
        else:
            rate /= 60;

    return timerank

def get_text(i, isTop):

    text = ""
    if isTop:
        line = lines_t[i]; i+=1;
        # print line;    
        while not line.isspace():
            text += line
            line = lines_t[i]; i+=1;

    else:
        line = lines_b[i]; i+=1;
                
        while not line.isspace():
            text += line
            line = lines_b[i]; i+=1;

    text = re.sub('\r\n', '\N', text)
    text = text[:-2] + '\n'

    return (text, i)

def write_remaining_lines(dst, i, isTop):
    if isTop:
        while 1:
            try:
                line_t = lines_t[i]; i+=1;
            except IndexError:
                return;

            if isNumber(line_t):
                time_t = lines_t[i]; i+=1;
                (text_t , i) = get_text(i, isTop=True);
                writetodst(time_t, text_t, dst, pos="Top");

    else:
        while 1:
            try:
                line_b = lines_b[i]; i+=1;
            except IndexError:
                return;

            if isNumber(line_b):
                time_b = lines_b[i]; i+=1;
                (text_b , i) = get_text(i, isTop=False);
                writetodst(time_b, text_b, dst, pos="Bot");



def srt2ass(srcFilepathTOP, srcFilepathBOTTOM, dstFilepath, isUTF16):

    dst = open(dstFilepath, 'w')

    dst.write("""[Script Info]
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
Timer: 100,0000
Video Aspect Ratio: 0
WrapStyle: 0
ScaledBorderAndShadow: no

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Arial,16,&H00FFFFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,10,0
Style: Top,Arial,16,&H00F9FFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,8,10,10,10,0
Style: Mid,Arial,16,&H0000FFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,5,10,10,10,0
Style: Bot,Arial,16,&H00F9FFF9,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,10,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n""");


    i_t, i_b = 0, 0;
    getnext_t = True
    getnext_b = False

    time_t, time_b = '', '';
    text_t, text_b = '', '';

    # Init time_b, text_b, and rank_b with first subtitle.
    while 1:
        line_b = lines_b[i_b]; i_b+=1;

        if isNumber(line_b):
            time_b = lines_b[i_b]; i_b+=1;
            rank_b = get_timerank(time_b);
            (text_b , i_b) = get_text(i_b, isTop=False);
            break;

    while 1:
        if getnext_t:

            try:
                line_t = lines_t[i_t]; i_t+=1;
            except IndexError:
                write_remaining_lines(dst, i_b, isTop=False);
                break;
            if isNumber(line_t):
                time_t = lines_t[i_t]; i_t+=1;
                rank_t = get_timerank(time_t);
                (text_t , i_t) = get_text(i_t, isTop=True);

                if rank_t < rank_b:
                    writetodst(time_t, text_t, dst, pos="Top");
                    getnext_t = True;
                    getnext_b = False;
                elif rank_b <= rank_t:
                    writetodst(time_b, text_b, dst, pos="Bot");
                    getnext_t = False;
                    getnext_b = True;

        if getnext_b:

            try:
                line_b = lines_b[i_b]; i_b+=1;
            except IndexError:
                write_remaining_lines(dst, i_t, isTop=True);
                break;
            if isNumber(line_b):
                time_b = lines_b[i_b]; i_b+=1;
                rank_b = get_timerank(time_b);
                (text_b , i_b) = get_text(i_b, isTop=False);

                if rank_b < rank_t:
                    writetodst(time_b, text_b, dst, pos="Bot");
                    getnext_b = True;
                    getnext_t = False;
                elif rank_t <= rank_b:
                    writetodst(time_t, text_t, dst, pos="Top");
                    getnext_b = False;
                    getnext_t = True;



    

if __name__ == '__main__':

    # define options for opening a file
    fileopts = {}
    fileopts['filetypes'] = [('srt files', '.srt')]
    fileopts['title'] = 'Choose first .srt file'

    root = Tkinter.Tk()
    root.withdraw()
    srcFilepath1 = tkFileDialog.askopenfilename(**fileopts)

    fileopts['title'] = 'Choose second .srt file'
    srcFilepath2 = tkFileDialog.askopenfilename(**fileopts)
    
    # defining options for saving dst file
    dstopts = {}
    dstopts['title'] = 'Choose filename for .ass file'
    dstopts['filetypes'] = [('ass files', '.ass')]
    dstopts['defaultextension'] = '.ass'
    dstopts['initialfile'] = 'output.ass'

    fTOP = codecs.open(srcFilepath1, "r")
    fBOTTOM = codecs.open(srcFilepath2, "r")
    lines_t = fTOP.readlines()
    lines_b = fBOTTOM.readlines()
    fTOP.close()
    fBOTTOM.close()


    dstFilepath = tkFileDialog.asksaveasfilename(**dstopts)

    srt2ass(srcFilepath1, srcFilepath2, dstFilepath, isUTF16=False)
