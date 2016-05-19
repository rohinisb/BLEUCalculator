import math
import codecs
import operator
import sys
import os

out = codecs.open("bleu_out.txt", "w", "utf-8")


# read lines from the candidate and reference files and store as a list
def read_input(path):
    input_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                input_txt = codecs.open(os.path.join(root, f), "r", "utf-8")
                input_list.append(input_txt.readlines())
    else:
        input_txt = codecs.open(path, "r", "utf-8")
        input_list.append(input_txt.readlines())
    return input_list


def compute_word_count(words, n, dic):
    ngram_len = len(words) - n + 1
    for j in range(ngram_len):
        ngram = ' '.join(words[j:j+n])
        if ngram in dic.keys():
            dic[ngram] += 1
        else:
            dic[ngram] = 1
    return dic, ngram_len


def compute_ngram_precision(candidate_list, reference_list, n):
    clipped_count = 0
    count = 0
    ref = 0
    cand = 0
    for i in range(len(candidate_list[0])):
        reference_word_count = []
        reference_length = []
        for reference in reference_list:
            word_count = dict()
            ref_sentence = reference[i]
            words = ref_sentence.strip().split()
            reference_length.append(len(words))
            word_count, ngram_len = compute_word_count(words, n, word_count)
            reference_word_count.append(word_count)
        cand_sentence = candidate_list[0][i]
        candidate_word_count = dict()
        words = cand_sentence.strip().split()
        candidate_word_count, ngram_len = compute_word_count(words, n, candidate_word_count)


def main():
    cand = read_input(sys.argv[1])
    ref = read_input(sys.argv[2])
    precision = []
    for i in range(4):
        pr, bp = compute_ngram_precision(cand, ref, i+1)
        precision.append(pr)


main()
