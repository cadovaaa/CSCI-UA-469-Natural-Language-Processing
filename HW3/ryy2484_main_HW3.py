import sys
from collections import defaultdict
import numpy as np
import math

#read file
if len(sys.argv) > 1:
    file_path = './' + sys.argv[1]
else: 
    file_path = './WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_24.pos'

f = open(file_path, 'r')
content = f.read()


#create dict within dicts of emissions, transitions and count tag frequency
emission_counts = defaultdict(lambda: defaultdict(int))
transition_counts = defaultdict(lambda: defaultdict(int))
tag_counts = defaultdict(int)
word_counts = defaultdict(int)

sentences = []
sentence = []

for line in content.splitlines():
    line = line.strip()

    if not line:
        if sentence:
            sentences.append(sentence)
            sentence = []
    else:  
        word, tag = line.split()
        #word = word.lower()
        sentence.append((word, tag))
if sentence:
    sentences.append(sentence)


for part in sentences:
    prev_tag = "Begin_Sent"

    for word, tag in part:
        emission_counts[tag][word] += 1
        transition_counts[prev_tag][tag] += 1
        word_counts[word] += 1
        tag_counts[tag] += 1

        prev_tag = tag

    transition_counts[prev_tag]["End_Sent"] += 1

#make prior probability table
prior_prob = {}
for tag1 in transition_counts:
    prior_prob[tag1] = {}
    
    total = sum(transition_counts[tag1].values())
    for tag2 in transition_counts[tag1]:
        prior_prob[tag1][tag2] = transition_counts[tag1][tag2] / total

#make likelihood table
likelihood = {}
for tag in emission_counts:
    likelihood[tag] = {}
    
    total = sum(emission_counts[tag].values())
    for word in emission_counts[tag]:
        likelihood[tag][word] = (emission_counts[tag][word] + 1) / (total + len(word_counts))

#define OOV item rules
def oov_prob(word, tag):
    if not word:
        return 1e-6
    if word[0].isupper() and tag == "NNP":
        return 1e-4
    if any(c.isdigit() for c in word) and tag == "CD":
        return 1e-3
    word = word.lower()
    if word.endswith("ing") and tag == "VBG":
        return 1e-4
    if word.endswith("ed") and tag == "VBD":
        return 1e-4
    if word.endswith("ly") and tag == "RB":
        return 1e-4
    if word.endswith("s") and tag in ["NNS", "VBZ"]:
        return 1e-4
    if word.endswith("ion") and tag == "NN":
        return 1e-4
    if word.endswith(("ous","ful","able","ive","al")) and tag == "JJ":
        return 1e-4
    return 1e-6

#define viterbi algorithm
def viterbi_hmm_tagger(words, states):
    T = len(words) #including "."
    N = len(states)-2 #including "Begin_Sent" and "End_Sent"

    viterbi = np.zeros((N+2, T))
    backpointer = np.zeros((N+2, T), dtype=int)

    #initialize matrix
    for q in range(1, N+1):
        a = prior_prob.get(states[0], {}).get(states[q], 1e-5)
        #b = likelihood.get(states[q], {}).get(words[0], oov_prob(words[0], states[q]))
        if words[0] in word_counts:
            b = likelihood.get(states[q], {}).get(words[0], 1e-8)
        else:
            b = oov_prob(word, states[q])
        viterbi[q][0] = a * b
        backpointer[q][0] = -1

    #traverse matrix
    for w in range(1, T):
        for q in range(1, N+1):
            probs = []
            for prev_q in range(1, N+1):
                a = prior_prob.get(states[prev_q], {}).get(states[q], 1e-5)
                #b = likelihood.get(states[q], {}).get(words[w], oov_prob(words[w], states[q]))
                if words[w] in word_counts:
                    b = likelihood.get(states[q], {}).get(words[w], 1e-8)
                else:
                    b = oov_prob(word, states[q])
                probs.append(viterbi[prev_q][w-1] * a * b)
            best = np.argmax(probs)
            viterbi[q][w] = probs[best]
            backpointer[q][w] = best + 1

    #calculate final probabilities
    final_probs = []
    for q in range(1, N+1):
        a = prior_prob.get(states[q], {}).get("End_Sent", 1e-5)
        final_probs.append(viterbi[q][T-1] * a)
    best = np.argmax(final_probs) + 1

    #backtrace
    best_path = [best]
    for w in range(T-1, 0, -1):
        best_state = backpointer[best_path[-1], w]
        best_path.append(best_state)
    best_path.reverse()

    best_states = [states[i] for i in best_path]
    return best_states, viterbi


#tag sentence
if len(sys.argv) > 2:
    file_path = './' + sys.argv[2]
else: 
    file_path = './WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_24.words'

f = open(file_path, 'r')
content = f.read()

sentences = []
sentence = []

for line in content.splitlines():
    line = line.strip()

    if not line:
        if sentence:
            sentences.append(sentence)
            sentence = []
    else:
        sentence.append(line)
if sentence:
    sentences.append(sentence)


states = ["Begin_Sent"]
states += list(tag_counts.keys())
states.append("End_Sent")


for words in sentences:
    #words_lower = [word.lower() for word in words]
    
    #tags = viterbi_hmm_tagger(words=words_lower, states=states)[0]
    tags = viterbi_hmm_tagger(words=words, states=states)[0]
    for i in range(len(words)):
        print(words[i] + "\t" + tags[i])
    print("")
