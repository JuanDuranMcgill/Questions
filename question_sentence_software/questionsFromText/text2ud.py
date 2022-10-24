#!/usr/bin/env python3

##  Python 3 filter from transforming an English or French sentence (on a single line) 
##   given as stdin to a UD in conllu format returned on stdout
##   it uses the Stanza parser (https://stanfordnlp.github.io/stanza/)
##   which must first be installed with "pip3 install stanza"
##   and the English/French modules must have been  preloaded 
##   with "stanza.download('en')" or "stanza.download('fr')"
##  the single argument to the program indicates the language en|fr (default en)

import sys,os,re,datetime
import stanza
from stanza.utils.conll import CoNLL


def text2ud(id,nlp,text):
    res=[]
    doc=nlp(text)
    sentences=doc.sentences    
    for i,ud in enumerate(CoNLL.convert_dict(doc.to_dict())):
        res.append("# sent_id = %s.%d"%(id,i))
        res.append("# text = %s"%sentences[i].text)
        for l in ud:
            l[9]="_"    # ignore last field (start_char,end_char)
            res.append("\t".join(l))
        res.append("")
    return res

## taken from http://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
def modificationDate(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)
    
##  process file.txt to create file.conllu if it does not exist or is older than file.txt
def processFile(txtFileName,lang="en"):
    txtF=open(txtFileName,"r",encoding="utf-8")
    txtDate=modificationDate(txtFileName);
    conlluFileName=re.sub(".txt$",".conllu",txtFileName)
    processors='tokenize,pos,lemma,depparse'
    if lang=="fr":processors+=',mwt'
    nlp = stanza.Pipeline(lang,processors=processors,verbose=False)
    conlluF=open(conlluFileName,"w",encoding="utf-8")
    no=1
    for line in txtF:
        conlluF.write("\n".join(text2ud(no,nlp,line)))
        conlluF.write("\n")
        no+=1
    conlluF.close()

# showUD("test","Barack Obama was born in Hawaii." + "He was elected president in 2008.")
# showUD("test-1","Barack Obama was born in Hawaii.")
# showUD("test-2","He was elected president in 2008.")

def main():
    lang="en"
    if len(sys.argv)>1:
        lang=sys.argv[1]
        if lang!='en' and lang!='fr':
            print('only en and fr supported')
            sys.exit(1)
    if len(sys.argv)>2:
        processFile(sys.argv[2])
        sys.exit()
    
    ### process stdin and print on stdout
    processors='tokenize,pos,lemma,depparse'
    if lang=="fr":processors+=',mwt'
    nlp = stanza.Pipeline(lang,processors=processors,verbose=False)
    
    no=0
    lines=sys.stdin.readlines()
    for line in lines:
        no+=1
        print("\n".join(text2ud("id-%s"%no,nlp,line.strip())))

if __name__ == '__main__':
    main()