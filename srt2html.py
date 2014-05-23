
import codecs
import os
import unicodedata as ud

# --- USER VARIABLES -----------------
# Declare source directory for subtitles to convert
srcDir = "~/Desktop/a/"
# Declare destination directory for html files
dstDir = "~/Desktop/b/"

latin_letters= {}


# --- HELPER FUNCTIONS -------------
def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha()) # isalpha suggested by John Machin


def isNumber(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

# --- CONVERSION FUNCTION --------------
def srt2html(srcFilepath, dstFilepath):
    src = codecs.open(srcFilepath, 'r')
    dst = open(dstFilepath, 'w')

    dst.write("""
    <!DOCTYPE html> 
    <html>
    <head>
        <title>HTML subs</title> 
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
        <style type="text/css">
    
        body {
            background-color: aliceblue;
            font-size: 16pt;
            color: #EE4000;
            font-family: 'MS PGothic', Osaka, Arial, sans-serif;
        }

        p {
            margin-bottom: 2em;
        }

        </style>
    </head> 
     
    <body> 
            
    """)
    srcLines = src.readlines()

    for i, line in enumerate(srcLines):
        # print only_roman_chars(line)
        # if(only_roman_chars(line) == False):
        if(isNumber(line)):
            dst.write("""
            <p>
            """ + srcLines[i+2] + 
            "</p>")

    dst.write("""
            
        </body>
        </html>
    """)

if __name__ == '__main__':

    for root, dirs, files in os.walk(os.path.expanduser(srcDir)):

        # Ignore hidden files and directories.
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for name in files:
            fname, fext = os.path.splitext(name)#'.'.join((name.split('.'))[:-1]);
            srcFilepath = os.path.expanduser(srcDir + name);
            dstFilepath = os.path.expanduser(dstDir + fname + ".html") 
            srt2html(srcFilepath, dstFilepath);

