This folder contains the evaluation scripts used to compute accuracy scores for UnifiedQA and other fine-tuned models. All requirements are listed in the requirements.txt file.

To run the evaluation, please use:
./t5_eval.sh <output_file> <mcqa_file>

where <output_file> is a tsv file containing both inputs and outputs of your model (one line per question) in the following format:

Who proposed the theory of evolution by natural selection? \n (A) linnaeus (B) scopes (C) shaw (D) darwin	darwin

and <mcqa_file> is a jsonl reference file with each line formated as follow:

{"question": {"stem": "Who proposed the theory of evolution by natural selection?", "choices": [{"text": "linnaeus", "label": "A"}, {"text": "scopes", "label": "B"}, {"text": "shaw", "label": "C"}, {"text": "darwin", "label": "D"}]}, "answerKey": "D"}

Of course, the lines in both files should match
