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

def question_processing(sentences,token):
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

