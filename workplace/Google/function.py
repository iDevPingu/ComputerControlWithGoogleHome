import tensorflow as tf
from konlpy.tag import Okt
from collections import Counter
import pandas as pd
import numpy as np
import gensim
from matplotlib import pyplot as plt
from vectorizer import BaseVectorizer

keras = tf.keras

MAX_LENGTH = 10
def tokenize_and_filter(sentences, labels):
    inputs, outputs = [], []
  
    for sentence, label in zip(sentences, labels):
    # tokenize sentence
        tokenized_sentence = tokenizer.encode_a_doc_to_list(sentence)
        
    # check tokenized sentence max length
        if len(tokenized_sentence) <= MAX_LENGTH:
            inputs.append(tokenized_sentence)
#             print("input append")
            outputs.append(label_to_id[label])
  
  # pad tokenized sentences
    padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(
        inputs, maxlen=MAX_LENGTH, padding='post', 
        value = tokenizer.vocabulary_['_PAD_']) # value = 0
  
    return padded_inputs, outputs

def tokenize_by_char(words,labels):
    inputs , outputs = [], []
    for word,label in zip(words,labels):
        tempword = []
        tempnum = []
        for i in range(len(word)):
            tempword.append(word[i])
        for i in tempword:
            tempnum.append(wordvoca[i])
        if len(tempnum) <= MAX_LENGTH:
            inputs.append(tempnum)
            outputs.append(label_to_id[label])
    padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(
        inputs, maxlen=MAX_LENGTH, padding='post', 
        value = tokenizer.char2idx['_PAD_']) # value = 0
  
    return padded_inputs, outputs


def decode_num_char(wordvoca,inputs):
    result = []
    for i in range(len(inputs)):
        for j in wordvoca.keys():
            try:
                if wordvoca[j] == inputs[i]:
                    result.append(j)
                else:
                    pass
            except:
                result.append('')

    return result
def Entity_question_processing(words, token):
    MAX_LENGTH = 10
    inputs = [] 
    wordvoca = token.char2idx
    for word in words:
        tempword = []
        tempnum = []
        for i in range(len(word)):
            tempword.append(word[i])
        for i in tempword:
            try:
                tempnum.append(wordvoca[i])
            except:
                pass
        if len(tempnum) <= MAX_LENGTH:
            inputs.append(tempnum)
        else:
            print("단어의 길이가 너무 길어요")
    padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(
    inputs, maxlen=MAX_LENGTH, padding='post', 
    value = token.char2idx['_PAD_']) # value = 0
    return padded_inputs

def Intent_question_processing(sentences,token):
    inputs = []
    
    for sentence in sentences:
        # tokenize sentence
        tokenized_sentence = token.encode_a_doc_to_list(sentence)
        # check tokenized sentence max length
        if len(tokenized_sentence) <= MAX_LENGTH:
            inputs.append(tokenized_sentence)
        else:
            print('입력이 너무 길어요.')
    # pad tokenized sentences
    padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(
    inputs, maxlen=MAX_LENGTH, padding='post', 
    value = token.vocabulary_['_PAD_']) # value = 0
    return padded_inputs

def tokenizer():
    t = Okt()
    token = BaseVectorizer(t.morphs)
    return token

