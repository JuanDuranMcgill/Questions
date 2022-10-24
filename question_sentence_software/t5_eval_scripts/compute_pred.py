import argparse
import nltk
from nltk.tokenize import word_tokenize
from tqdm import tqdm
import jsonlines
import numpy as np

import sys
nltk.download('punkt')

def similarity(x, y):
    return len(set(x).intersection(y))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv_file")
    parser.add_argument("mcqa_file")
    parser.add_argument("pred_file")

    args = parser.parse_args()

    #tokenizer = AutoTokenizer.from_pretrained("allenai/unifiedqa-t5-large")

    print("***Computing predictions for {} with reference {}...".format(args.tsv_file, args.mcqa_file))
    print("***Writing to {}...".format(args.pred_file))
   
    with open(args.pred_file, 'w') as out_f:
        tsv = open(args.tsv_file, 'r')
        for mcqa_line in jsonlines.open(args.mcqa_file, 'r'):
            tsv_line = tsv.readline()
            generated_tokens = word_tokenize(tsv_line.split('\t')[1].lower())
            choices_tokens = [word_tokenize(ch["text"].lower()) for ch in mcqa_line["question"]["choices"]]

            choices_similarity = [similarity(generated_tokens, ch) for ch in choices_tokens]
            selection = np.argmax(choices_similarity)

            out_f.write("{}\n".format(mcqa_line["question"]["choices"][selection]["label"]))
        out_f.close()
        tsv.close()
