import sys
import random
import json
import nltk
from nltk.corpus import stopwords
import time

t1=time.time()

nltk.download('stopwords')
blacklist = stopwords.words('english')

def build_answers_dict(lines):
    answers_dict = dict()
    for line in lines:
        if len(line) > 2 and line[2] == 'W':
            ans_type = line[2:5]
            ans = line.split('=>')[-1].strip()
            if ans.lower() in blacklist:
                continue
            if ans_type in answers_dict:
                answers_dict[ans_type].append(ans)
            else:
                answers_dict[ans_type] = [ans]
    return answers_dict


file_in = open(sys.argv[1], 'r')
file_out = open(sys.argv[2], 'w')
file_meta = open("{}.meta.tsv".format('.'.join(sys.argv[2].split('.')[:-1])), 'w')
file_dict = open("{}_dict.json".format('.'.join(sys.argv[2].split('.')[:-1])), 'w')

lines = file_in.readlines()

answers_dict = build_answers_dict(lines)
json.dump(answers_dict, file_dict)
file_dict.close()

for line in lines:
    if len(line) > 2 and line[2] == 'W':
        ans_type = line[2:5]
        line = line.split('= ')[1]
        line = line.split('=>')
        question = line[0].strip()
        answer = line[1][:-1].strip()
        if answer.lower() in blacklist:
            continue
        answers = [answer]
        for _ in range(3):
            answers.append(random.choice(answers_dict[ans_type]))
        random.shuffle(answers)
        file_out.write("{} \\n (A) {} (B) {} (C) {} (D) {}\t{}\n".format(question, answers[0], answers[1], answers[2], answers[3], answer))
        file_meta.write("{}\t{}\t{}\n".format(question, answer, ans_type))
file_in.close()
file_out.close()
t2 = time.time()

print("It took ",t2-t1," seconds.")
