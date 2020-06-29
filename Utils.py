import re
def split_text_max_words(lines, max_words):
    sentences = []

    for line in lines:
        splits = re.finditer("\. [A-Z]|\.\n", line)
        last_split_idx = 0
        for split in  splits:
            sentence = line[last_split_idx: split.start() + 1]
            if(len(sentence.split(" ")) >= 5):
                 sentences.append(sentence)
            last_split_idx = split.start() + 2
                
    sentence_splitted_by_max_words = []

    for sentence in sentences:
        words = sentence.split(" ")

        for i in range(len(words) // max_words):
            begin = i*max_words
            end = (i+1)*max_words
            sentence_splitted_by_max_words.append(" ".join(words[begin : end]))
        
        if(len(words) % max_words != 0):
            begin = (len(words) // max_words)*max_words
            end = (len(words) // max_words)*max_words + (len(words) % max_words)
            sentence_splitted_by_max_words.append(" ".join(words[begin : end]))

    return sentence_splitted_by_max_words
