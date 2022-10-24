import jsonlines
import sys

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(output_file, 'w') as f:
        for line in jsonlines.open(input_file, 'r'):
            ans = ""
            ansKey = line["answerKey"]

            out_line = line["question"]["stem"]
            out_line += " \\n"
            for choice in line["question"]["choices"]:
                out_line += " ({}) {}".format(choice["label"], choice["text"])
                if choice["label"] == ansKey:
                    ans = choice["text"]

            assert ans != ""
            f.write("{}\t{}\n".format(out_line, ans))

        f.close()
