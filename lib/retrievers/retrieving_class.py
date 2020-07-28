# Import the Libraries
from numpy import dot
from numpy.linalg import norm
import copy
import pandas as pd
import sys
import math
from pathlib import Path

parent_dir = str(Path(__file__).parents[2])
sys.path.insert(0, parent_dir)

from lib.helpers.utils import split


class RetrieveEmb():

    def __init__(self, emb_dict):
        self.emb_dict = emb_dict
        self.words_list_dict = self.emb_dict.keys()


    def cosine_sim_query_quotes(self, user_query_embedding, retrieve_emb_dict, method):
        '''
        Find Cosine similarity of two vectors
        :param emb_dict: file containing the embedding dictionary
        :param user_question: question asked by the user
        :return: The cosine similarity vectors with all quotes
        '''
        cos_scores_list = []

        for r_id, r_embedding_author_list_of_list in retrieve_emb_dict.items():

            if method != 'queries':
                r_embedding_author_list_of_list = [r_embedding_author_list_of_list]

            else:
                chunks = int(len(r_embedding_author_list_of_list) / 4)
                r_embedding_author_list_of_list = list(split(r_embedding_author_list_of_list, chunks))

            for r_embedding_author_list in r_embedding_author_list_of_list:

                r_embedding = r_embedding_author_list[0]
                r_author = r_embedding_author_list[1]
                r_sentence = r_embedding_author_list[-1]

                if len(r_embedding_author_list) == 4: #use_bow_simple_avg_hm_queries
                    r_hm_query = r_embedding_author_list[2]

                cosine_score = dot(user_query_embedding, r_embedding) / (norm(user_query_embedding) * norm(r_embedding))
                cosine_score = round(cosine_score, 2)
                cos_scores_item = [cosine_score, r_sentence, r_author, r_id]

                if len(r_embedding_author_list) == 4:  # use_bow_simple_avg_hm_queries
                    cos_scores_item = [cosine_score, r_sentence, r_author, r_hm_query, r_id]

                if math.isnan(cos_scores_item[0]):
                    continue

                cos_scores_list.append(cos_scores_item)

        unsorted_cos_scores_list = copy.deepcopy(cos_scores_list)

        cos_scores_list.sort(key=lambda k: k[0], reverse=True)

        return cos_scores_list, unsorted_cos_scores_list



    def extract_top_retrievals(self, cos_scores_list_sorted, max_num = 1):

        '''
        From a sorted list of similarity scores, extract the top retrievals
        :param cos_scores_list_sorted:
        :param max_num:
        :return:
        '''

        top_retrievals = cos_scores_list_sorted[:max_num]

        return top_retrievals



