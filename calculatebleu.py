import codecs
import sys
import os

out = codecs.open("bleu_out.txt", "w", "utf-8")


def read_input(path):
    input_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                input_txt = codecs.open(file, "r", "utf-8")
                input_list.append(input_txt.readlines())
    else:
        input_txt = codecs.open(path, "r", "utf-8")
        input_list = input_txt.readlines()
    return input_list


def main():
    cand = read_input(sys.argv[1])
    ref = read_input(sys.argv[2])
    print cand, ref


main()
