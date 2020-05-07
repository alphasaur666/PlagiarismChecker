import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
import bert
import pandas as pd
import numpy as np
import re
import random
import math


def preprocess_text(sen):
    
    #Removing htmls
    sentence = remove_tags(sen)

    # Remove punctuations and numbers using regex
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal using regex
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    # Removing multiple spaces using regex
    sentence = re.sub(r'\s+', ' ', sentence)

    return sentence

TAG_RE = re.compile(r'<[^>]+>') #cleans

def remove_tags(text):
    return TAG_RE.sub('',text)


BertTokenizer = bert.bert_tokenization.FullTokenizer
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1" ,trainable = False)
vocabulary_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
to_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = BertTokenizer(vocabulary_file, to_lower_case)



tokenizer.tokenize("don't be so judgemental") # testing tokens on hardcoded output