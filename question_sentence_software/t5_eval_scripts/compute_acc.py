import sys
import jsonlines
from tqdm import tqdm


if __name__ == "__main__":
    mcqa_file = sys.argv[1]
    pred_file = sys.argv[2]

    nb_true = 0
    nb_questions = 0

    print("***Calculating accuracy for {} with reference {}...".format(pred_file, mcqa_file))

    with open(pred_file, 'r') as f:
        for mcqa_line in jsonlines.open(mcqa_file, 'r'):
            nb_questions += 1
            if f.readline()[:-1] == mcqa_line["answerKey"]:
                nb_true += 1

    acc = nb_true / nb_questions
    print("--> accuracy: {}".format(acc))
