from lib.helpers.preprocessing_class import DataProcessing
import json
import sys
import os
from pathlib import Path

parent_dir = str(Path(__file__).parents[1])
sys.path.insert(0, parent_dir)

with open(os.path.join(parent_dir, 'data','split','split-conceptnet','fileCustomWords')) as json_file:
    custom_words_dict = json.load(json_file)

with open(os.path.join(parent_dir, 'data','split','split-hashmap','conceptnet_distribution.json')) as json_file:
    conceptnet_distribution = json.load(json_file)

with open(os.path.join(parent_dir, 'data','output', 'dictionaries', 'hmq_quotes_emb_dict')) as json_file:
    hmq_quotes_emb_dict = json.load(json_file)


class GatheringEmbeddingsClass():
    def __init__(self, user_query):
        # ToDO: Global declaration can mess up
        self.user_query = user_query
        self.user_query_embeddings = {}
        self.words = []
        self.embeddings = {}

    def tokenize_query(self, query):
        dp = DataProcessing()
        query_tokens = dp.tokenize_sentence(dp.sentence_cleaning(query))

        return query_tokens

    def run_embeddings(self):
        custom_words = []
        non_custom_words = []
        embeddings = {}
        query_tokens = self.tokenize_query(self.user_query)

        for q in query_tokens:
            if q in custom_words_dict.keys():
                custom_words.append(q)
            else:
                non_custom_words.append(q)

        for word in custom_words:
            #embeddings[word] = json.loads(custom_words_dict[word])
            embeddings[word] = custom_words_dict[word]

        for word in non_custom_words:
            #print('--------> ', word)
            first_letter = word[0]
            second_letter = word[1]
            if type(conceptnet_distribution[first_letter]) == dict:
                if first_letter+second_letter in conceptnet_distribution[first_letter].keys():
                    file_suffix = first_letter.upper()+second_letter.upper()
                    with open(os.path.join(parent_dir, 'data','split','split-conceptnet', 'sub-file' + file_suffix)) as json_file:
                        embeddings_file = json.load(json_file)

                    embeddings[word] = embeddings_file[word]
                else:
                    file_suffix = first_letter.upper()
                    with open(os.path.join(parent_dir, 'data', 'split', 'split-conceptnet', 'sub-file' + file_suffix)) as json_file:
                        embeddings_file = json.load(json_file)

                    embeddings[word] = embeddings_file[word]
            else:
                file_suffix = first_letter.upper()
                with open(os.path.join(parent_dir, 'data','split','split-conceptnet','file' + file_suffix)) as json_file:
                    embeddings_file = json.load(json_file)

                embeddings[word] = embeddings_file[word]

        #print('custom_words', custom_words)
        #print('non_custom_words', non_custom_words)

        self.words = custom_words + non_custom_words
        self.embeddings = embeddings


    def sentence_embedding(self, idf_dict, stop_words):

        '''
        Given a single sentence, compute it's embeddings
        :param sentence:
        :param emb_dict:
        :param words_list_dict:
        :return:
        '''
        self.run_embeddings()
        embeddings = self.embeddings

        sen_emb = [0] * 300
        word_count = 0

        for word in self.words:
            if word not in idf_dict:
                   idf_score = 1.0
            else:
                   idf_score = idf_dict[word]

            if word in stop_words:
                idf_score = 0.1

            #word_emb = embeddings[word].values()
            word_emb = embeddings[word]

            word_emb_idf_weighted = [i * idf_score for i in word_emb]
            word_count = word_count + 1
            sen_emb = [sum(x) for x in zip(sen_emb,  word_emb_idf_weighted )]

        #if word_count > 0:
        #   sen_emb = list(map(lambda x: round(x / word_count, 3), sen_emb))

        return sen_emb



#
#
# gec = GatheringEmbeddingsClass(user_query='Who am I')
#
# emb = gec.sentence_embedding(hmq_quotes_emb_dict)
# print(emb)