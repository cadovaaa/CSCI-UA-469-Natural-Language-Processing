Instructions for running my system:
For training and test files with paths from the present working directory 
file1 and file2 respectively, type the following into the terminal:
python ryy2484_viterbi_HW3.py file1 file2 > submission.terminal
This will train the model and predict tags for the words in the test file.

If no files are specified, it will use WSJ_24.pos and WSJ_24.words as 
the training and test files respectively. 


OOV handing:
I handled OOV items by using La Place smoothing in combination with filtering 
for capital letters and the beginning of the word, digits, and certain word endings.

This allowed me to ensure no probability would be 0. It also allowed me to 
categorize OOV items based on certain traits specific types of words were more
likely to have.
