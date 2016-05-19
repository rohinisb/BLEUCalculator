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


def compute_clipped_count(candidate_count, references_count):
    clipped_count = 0
    for ngram in candidate_count.keys():
        ngram_count = candidate_count[ngram]
        max_count = 0
        for ref in references_count:
            if ngram in ref:
                max_count = max(max_count, ref[ngram])
        ngram_count = min(ngram_count, max_count)
        clipped_count += ngram_count
    return clipped_count


def best_length_match(candidate_length, ref_length):
    least_diff = abs(candidate_length - ref_length[0])
    best = ref_length[0]
    for ref in ref_length:
        if abs(candidate_length-ref) < least_diff:
            least_diff = abs(candidate_length - ref)
            best = ref
    return best


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
        clipped_count += compute_clipped_count(candidate_word_count, reference_word_count)
        count += ngram_len
        ref += best_length_match(len(words), reference_length)
        cand += len(words)


def main():
    cand = read_input(sys.argv[1])
    ref = read_input(sys.argv[2])
    precision = []
    for i in range(4):
        pr, bp = compute_ngram_precision(cand, ref, i+1)
        precision.append(pr)


main()
