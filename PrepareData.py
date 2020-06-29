import os
import Utils

def load_data():

    files = []
    documents = []
    path = 'Data/Plagiarism Documents';
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                files.append(path+'/'+file)


    for path in files:
        file = open(path ,'r')
        lines = file.readlines()
        documents.append(Utils.split_text_max_words(lines, 128))
        
    return documents


    

