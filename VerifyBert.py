from sentence_transformers import SentenceTransformer
import scipy.spatial
import numpy as np
import PrepareData

embedder = SentenceTransformer('output/training_stsbenchmark_bert-base-uncased-2020-06-19_19-51-26')

corpus = PrepareData.load_data()

# Corpus with example sentences
corpus_embeddings = []
for document in corpus:
    sentences_embeddings = embedder.encode(document)
    sentences_embeddings = np.array(sentences_embeddings)
    document_embedding = np.mean(sentences_embeddings, axis = 0)
    corpus_embeddings.append(document_embedding)


# Query sentences:
#
#similarity_matrix = []
#for first_doc in corpus_embeddings:
#    similarity_vector = []
#    for second_doc in corpus_embeddings:
#        similarity_vector.append(1 - scipy.spatial.distance.cosine(first_doc, second_doc))
#    similarity_matrix.append(similarity_vector)
#
#similarity_matrix = np.array(similarity_matrix)
#print(similarity_matrix)

        


# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
closest_n = 5
index = 0
for query, query_embedding in zip(corpus, corpus_embeddings):
    distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    print("\n\n======================\n\n")
    print("Document query index:", index)
    print("\nMost similar document in corpus:")

    for idx, distance in results[0:closest_n]:
        
        print(corpus[idx][0], "(Score: %.4f)" % (1-distance))

    index = index + 1
