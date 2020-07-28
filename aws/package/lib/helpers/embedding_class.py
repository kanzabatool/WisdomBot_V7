# Import the Libraries
import math
import pandas as pd
from collections import defaultdict
from lib.helpers.preprocessing_class import DataProcessing
from sklearn.feature_extraction.text import CountVectorizer


class GetEmbeddings():
    # Class to compute embeddings

    def __init__(self, emb_dict):
        self.emb_dict = emb_dict
        self.vocab = self.emb_dict.keys()


    def sentences_list_embedding(self, processed_sentence_list, sentence_list, author_list, quote_col_list, id_col_list, idf_dict, stop_words):

        '''
        Given a list of sentences, compute sentence embeddings
        :param sentence_list:
        :param emb_dict: pretrained embedding dictionary, {key = 'word', value = emb_vec}
        :return:
        '''

        sent_dict = defaultdict(str)

        dp = DataProcessing()

        for processed_sentence, sentence, author, quote, id in zip(processed_sentence_list, sentence_list, author_list, quote_col_list, id_col_list):

            sentence = dp.remove_starting_trailing_spaces(sentence)
            sen_emb = self.sentence_embedding(dp, processed_sentence, self.vocab, self.emb_dict, idf_dict, stop_words)

            if sentence == quote: #for use_bow_simple_avg_quotes
               #sent_dict[sentence] = [sen_emb, author]
               sent_dict[id] = [sen_emb, author, sentence]
            else: #for use_bow_simple_avg_hm_queries
               #sent_dict[quote] = [sen_emb, author, sentence, quote]
               if id in sent_dict:
                   sent_dict[id] = sent_dict[id] + [sen_emb, author, sentence, quote]
               else:
                   sent_dict[id] = [sen_emb, author, sentence, quote]

        return sent_dict



    def sentence_embedding(self, dp, sentence, vocab, emb_dict, idf_dict, stop_words):

        '''
        Given a single sentence, compute it's embeddings
        :param sentence:
        :param emb_dict:
        :param words_list_dict:
        :return:
        '''

        sentence_tokens  = dp.tokenize_sentence(sentence)
        sen_emb = [0] * 300
        word_count = 0

        for j, word in enumerate(sentence_tokens):
            if word in vocab:
                #if word in stop_words:
                    #idf_score = 0.1
                #else:
                if word not in idf_dict:
                       idf_score = 2.0
                else:
                       idf_score = idf_dict[word]
                word_emb = emb_dict[word]
                word_emb_idf_weighted = [i * idf_score for i in word_emb]
                word_count = word_count + 1
                sen_emb = [sum(x) for x in zip(sen_emb,  word_emb_idf_weighted )]

        if word_count > 0:
           sen_emb = list(map(lambda x: round(x, 3), sen_emb))

        return sen_emb


    def compute_tf_idf(self, dp, lines):

        #lines = ['I want to love', 'I want to live', 'Can you tell what do you want?']

        #query = 'I want to dance'

        #text_continous = ' '.join(lines).lower()

        #text = dp.tokenize_sentence(text_continous)

        #lines_tok = [' '.join(dp.tokenize_sentence(line)).lower() for line in lines]

        vec = CountVectorizer()
        X = vec.fit_transform(lines)
        count_df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())

        word_idf_dict = self.compute_word_tfidf_core(count_df)

        return word_idf_dict


    def compute_word_tfidf_core(self, word_count_matrix):

        #stop_words = read_lines('../data/axillary/custom_stopwords')

        words = list(word_count_matrix)
        word_idf_dict = defaultdict(str)
        total_docs = word_count_matrix.shape[0]

        for word in words:

            #if word in stop_words:
            #    idf = 0.1
            #    word_idf_dict[word] = idf
            #    continue

            counts = list(word_count_matrix[word])
            freq = sum(counts)
            appearances = sum(x > 0 for x in counts)

            tf = freq
            idf = abs(math.log10(appearances/total_docs))

            word_idf_dict[word] = round(idf, 3)

        return word_idf_dict
