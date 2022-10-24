import numpy as np
import sys
import nltk
from tqdm import tqdm
from nltk.corpus import stopwords
from collections import OrderedDict

nltk.download('stopwords')
blacklist=stopwords.words('english')

from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch

#model_name = 'cointegrated/rubert-tiny'
model_name = 'bert-base-uncased'
model = AutoModelForMaskedLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def score(model, tokenizer, sentence):
    tensor_input = tokenizer.encode(sentence, return_tensors='pt')
    repeat_input = tensor_input.repeat(tensor_input.size(-1)-2, 1)
    mask = torch.ones(tensor_input.size(-1) - 1).diag(1)[:-2]
    masked_input = repeat_input.masked_fill(mask == 1, tokenizer.mask_token_id)
    labels = repeat_input.masked_fill( masked_input != tokenizer.mask_token_id, -100)
    with torch.inference_mode():
        loss = model(masked_input, labels=labels).loss
    return np.exp(loss.item())





#print(score(sentence='What is the difference between a walrus and a cat?', model=model, tokenizer=tokenizer)) 
# 4.541251105675365
#print(score(sentence='What that, which for me is a doobe, baby?', model=model, tokenizer=tokenizer)) 
# 6.162017238332462







file_in = open(sys.argv[1], 'r')
lines = file_in.readlines()







WHE =  []
aWHE = []
pWHE = []
sWHE=[]

WAD = []
aWAD = []
pWAD = []
sWAD = []

WAS = [] 
aWAS = []
pWAS = []
sWAS = []

WAI = []
aWAI = []
pWAI = []
sWAI = []


i=0
qdic=dict()

currentSentence=""
for line in tqdm(lines):
    if len(line)>2 and line[2]=="T":
        currentSentence =  line.split('=')[-1].strip()
    if len(line)>2 and line[2].lower()=="w":
        ans = line.split('=>')[-1].strip()
        que = line.split('=')[1].strip()
        if ans.lower() in blacklist:
            continue
        i+=1
        qtype=line[2:5]
        if qtype=="WHE":
            WHE.append(que)
            aWHE.append(ans)
            sWHE.append(currentSentence)
        if qtype == "WAD":
            WAD.append(que)
            aWAD.append(ans)
            sWAD.append(currentSentence)
        if qtype == "WAS":
            WAS.append(que)
            aWAS.append(ans)
            sWAS.append(currentSentence)
        if qtype == "WAI":
            WAI.append(que)
            aWAI.append(ans)
            sWAI.append(currentSentence)

for q in tqdm(WAI):
    pWAI.append(score(model,tokenizer,q))
for q in tqdm(WAD):
    pWAD.append(score(model,tokenizer,q))
for q in tqdm(WAS):
    pWAS.append(score(model,tokenizer,q))
for q in tqdm(WHE):
    pWHE.append(score(model,tokenizer,q))


tWAI = list(zip(WAI, aWAI, sWAI))    
dWAI = dict(zip(pWAI,tWAI))
dWAI = dict(OrderedDict(reversed(sorted(dWAI.items()))))

tWAD = list(zip(WAD, aWAD, sWAD))
dWAD = dict(zip(pWAD,tWAD))
dWAD = dict(OrderedDict(reversed(sorted(dWAD.items()))))

tWAS = list(zip(WAS, aWAS, sWAS))
dWAS = dict(zip(pWAS,tWAS))
dWAS = dict(OrderedDict(reversed(sorted(dWAS.items()))))

tWHE = list(zip(WHE, aWHE, sWHE))
dWHE = dict(zip(pWHE,tWHE))
dWHE = dict(OrderedDict(reversed(sorted(dWHE.items()))))


with open("WHE.txt","w") as f:
    for i in dWHE:
        f.write("Sentence: ")
        f.write(dWHE[i][2])
        f.write("\n")
        f.write("Question: ")
        f.write(dWHE[i][0])
        f.write("\n")
        f.write("Answer: ")
        f.write(dWHE[i][1])
        f.write("\n")
        f.write("Question Perp: ")
        f.write(str(i))
        f.write("\n")
        f.write("\n")
f.close()

with open("WAD.txt","w") as f:
    for i in dWAD:
        f.write("Sentence: ")
        f.write(dWAD[i][2])
        f.write("\n")
        f.write("Question: ")
        f.write(dWAD[i][0])
        f.write("\n")
        f.write("Answer: ")
        f.write(dWAD[i][1])
        f.write("\n")
        f.write("Question Perp: ")
        f.write(str(i))
        f.write("\n")
        f.write("\n")
f.close()

with open("WAS.txt","w") as f:
    for i in dWAS:
        f.write("Sentence: ")
        f.write(dWAS[i][2])
        f.write("\n")
        f.write("Question: ")
        f.write(dWAS[i][0])
        f.write("\n")
        f.write("Answer: ")
        f.write(dWAS[i][1])
        f.write("\n")
        f.write("Question Perp: ")
        f.write(str(i))
        f.write("\n")
        f.write("\n")
f.close()         

with open("WAI.txt","w") as f:
    for i in dWAI:
        f.write("Sentence: ")
        f.write(dWAI[i][2])
        f.write("\n")
        f.write("Question: ")
        f.write(dWAI[i][0])
        f.write("\n")
        f.write("Answer: ")
        f.write(dWAI[i][1])
        f.write("\n")
        f.write("Question Perp: ")
        f.write(str(i))
        f.write("\n")
        f.write("\n")
f.close() 


        
