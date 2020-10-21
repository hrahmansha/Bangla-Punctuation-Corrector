# coding: utf-8

from __future__ import division

import models, data, main

import re
import sys
import codecs
import tensorflow as tf
import numpy as np

def to_array(arr, dtype=np.int32):
    # minibatch of 1 sequence as column
    return np.array([arr], dtype=dtype).T

def convert_punctuation_to_readable(punct_token):
    if punct_token == data.SPACE:
        return " "
    else:
        return punct_token[0]

def punctuate(word_vocabulary, punctuation_vocabulary, reverse_punctuation_vocabulary, text, model):

    if len(text) == 0:
        sys.exit("Input text from stdin missing.")
        
    text = [w for w in text.split() if w not in punctuation_vocabulary] + [data.END]

    i = 0

    total_punctuation = len(data.PUNCTUATION_VOCABULARY)
    pred_text = ""
    while True:

        subsequence = text[i:i+data.MAX_SEQUENCE_LEN]

        if len(subsequence) == 0:
            break

        converted_subsequence = [word_vocabulary.get(w, word_vocabulary[data.UNK]) for w in subsequence]

        y = predict(to_array(converted_subsequence), model)

        pred_text += subsequence[0]
        print(subsequence[0], end="")

        last_eos_idx = 0
        punctuations = []
        for y_t in y:

            shape = tf.reshape(y_t, [-1])
            p_i = np.argmax(shape)
            # print(reverse_punctuation_vocabulary)
            # print(p_i%total_punctuation, y_t)
            # print(shape)
            # p_i = np.argmax(y_t.flatten())
            punctuation = reverse_punctuation_vocabulary[p_i%total_punctuation]

            punctuations.append(punctuation)

            if punctuation in data.EOS_TOKENS:
                last_eos_idx = len(punctuations) # we intentionally want the index of next element

        if subsequence[-1] == data.END:
            step = len(subsequence) - 1
        elif last_eos_idx != 0:
            step = last_eos_idx
        else:
            step = len(subsequence) - 1

        for j in range(step):
            pred_text += " " + punctuations[j] + " " if punctuations[j] != data.SPACE else " "
            print(" " + punctuations[j] + " " if punctuations[j] != data.SPACE else " ", end="")
            if j < step - 1:
                pred_text += subsequence[1+j]
                print(subsequence[1+j], end="")

        if subsequence[-1] == data.END:
            break

        i += step
    ff = codecs.open('tmpresults.txt', 'w', 'utf-8')
    ff.write(pred_text)
    return pred_text

def predict(x, model):
    return tf.nn.softmax(model(x))
