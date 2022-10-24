python3 compute_pred.py $1 $2 ./temp_pred.txt
python3 compute_acc.py $2 ./temp_pred.txt
rm ./temp_pred.txt
