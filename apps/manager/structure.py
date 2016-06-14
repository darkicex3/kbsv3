# import re
# from nltk.corpus import stopwords
# from collections import Counter
# import operator
#
#
# class Tree(object):
#     def __init__(self):
#         self.children = []
#         self.data = None
#
#
# def sentences_builder(objects):
#     sentences = []
#     new_sentences = []
#     final_sentences = []
#
#     for o in objects:
#         sentences.append(o.title.lower())
#
#     for sentence in sentences:
#         new_sentences.append(re.findall(r'\w+', sentence, flags=re.UNICODE | re.LOCALE))
#
#     for sentence in new_sentences:
#         important_words = []
#         for word in sentence:
#             if word not in stopwords.words('english'):
#                 important_words.append(word)
#         print(important_words)
#         final_sentences.append(important_words)
#         print(final_sentences)
#
#     return final_sentences
#
#
# def words_frequency_analyser(sentences):
#     words = []
#     for sentence in sentences:
#         for word in sentence:
#             words.append(word)
#
#     return Counter(words).most_common()
#
#
# def tree_builder(frequencies, sentences):
#
#     structure = Tree()
#
#     for counter in frequencies:
#         freqmax = frequencies[0][1]
#
#         if counter[1] == freqmax:
#             structure.data = counter[0]
            








