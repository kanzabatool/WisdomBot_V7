# Import the Libraries

# ToDo: Using timeit to find execution times, remove it when test is done
import time

import pandas as pd
import argparse
from collections import defaultdict
import os
import warnings
from pathlib import Path
import sys

parent_dir = str(Path(__file__).parents[4])
sys.path.insert(0, parent_dir)

from lib.helpers.utils import read_json, remove_items_from_list_given_indices
from lib.helpers.gathering_embeddings_class import GatheringEmbeddingsClass
from lib.retrievers.retrieving_class import RetrieveEmb
from lib.retrievers.miscellaneous_formatting import format_to_dict, format_to_frame

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='Wisdom Bot')
parser.add_argument('--user_query', help='query of the user presented to the bot',
                    default='How to gain wisdom?')

def get_default_args():

    parser = argparse.ArgumentParser(description='Wisdom Bot')
    parser.add_argument('--get_top_N_quotes', type=int, help='number of top quotes to extract',
                        default=2)
    parser.add_argument('--embedding_file', type=str, help='pretrained embedding file',
                        default='full_conceptnet_dict')

    parser.add_argument('--average_bow', help='use simple average bag of words embeddings of quotes method'
                        ,default=True)
    parser.add_argument('--queries', help='use simple average bag of words embeddings of human queries method'
                        ,default=True)
    parser.add_argument('--keywords', help='use simple average bag of words embeddings of human queries method'
                        ,default=True)
    parser.add_argument('--combined', help='use simple average bag of words embeddings of human queries method'
                        ,default=True)

    args = parser.parse_args()

    return args

def get_folders_paths(embedding_file):

    main_folder_path = Path(__file__).parents[1]

    output_dir = os.path.join(main_folder_path, 'data/output/dictionaries')
    axilliary_dir = os.path.join(main_folder_path, 'data/axillary')
    quotes_dir = os.path.join(main_folder_path, 'data/quotes')

    embedding_file = os.path.join(axilliary_dir, embedding_file)

    return output_dir, axilliary_dir, quotes_dir, embedding_file


def find_the_top_matched_quote(re, user_query_embedding, quotes_emb_dict, get_top_N_quotes):

    quotes = list(quotes_emb_dict.keys())

    sorted_quotes, unsorted_quotes = re.cosine_sim_query_quotes(user_query_embedding, quotes_emb_dict)
    top_quotes = re.extract_top_retrievals(sorted_quotes, max_num=get_top_N_quotes)

    return top_quotes, unsorted_quotes


def run_method(args, method_name, output_dir, q_emb_file, user_query_emb, user_query):

        q_emb_dict = read_json(os.path.join(output_dir, q_emb_file))

        re = RetrieveEmb(q_emb_dict)

        top_quotes, unsorted_quotes = find_the_top_matched_quote(re, user_query_emb, q_emb_dict, args.get_top_N_quotes)

        return top_quotes, unsorted_quotes


def run_all_chosen_methods(args, output_dir, user_query_emb, user_query):

    base_lines_used_dict = defaultdict(list)

    if args.average_bow:
        method_name = 'average_bow'
        top_quotes_1, unsorted_quotes_1 = run_method(args, method_name, output_dir, 'quotes_emb_dict', user_query_emb, user_query)
        base_lines_used_dict[method_name] = top_quotes_1

    if args.queries:
        method_name = 'queries'
        top_quotes_2, unsorted_quotes_2 = run_method(args, method_name, output_dir, 'hmq_quotes_emb_dict', user_query_emb, user_query)
        base_lines_used_dict[method_name] = top_quotes_2

    if args.keywords:
        method_name = 'keywords'
        top_quotes_3, unsorted_quotes_3 = run_method(args, method_name, output_dir, 'keywords_quotes_emb_dict', user_query_emb, user_query)
        base_lines_used_dict[method_name] = top_quotes_3

    if args.combined:
        method_name = 'combined'
        top_quotes_4 = reranker(args.get_top_N_quotes, method_name, unsorted_quotes_1, unsorted_quotes_2, unsorted_quotes_3, user_query)
        base_lines_used_dict[method_name] = top_quotes_4

    base_lines_used_dict = remove_duplicates_dict(base_lines_used_dict)

    return base_lines_used_dict


def remove_duplicates_dict(base_lines_used_dict):

     seen_quotes = []

     methods =  list(base_lines_used_dict.keys())

     for method in methods:
         method_info_list = base_lines_used_dict[method]
         idx_del_list = []
         for idx, method_info in enumerate(method_info_list):
             quote = method_info[1]
             if quote in seen_quotes:
                 seen_quotes = seen_quotes + quote
                 idx_del_list = idx_del_list + idx
         method_info_list = remove_items_from_list_given_indices(method_info_list, idx_del_list)

         base_lines_used_dict[method] = method_info_list

     return base_lines_used_dict




def reranker(get_top_N_quotes, method_name, unsorted_quotes_1, unsorted_quotes_2, unsorted_quotes_3, user_question):

    quotes = [quote_info[1] for quote_info in unsorted_quotes_1]
    authors = [quote_info[2] for quote_info in unsorted_quotes_1]
    cos1 = [quote_info[0] for quote_info in unsorted_quotes_1]
    cos2 = [quote_info[0] for quote_info in unsorted_quotes_2]
    cos3 = [quote_info[0] for quote_info in unsorted_quotes_3]

    quotes_all = pd.DataFrame(list(zip(quotes, authors, cos1, cos2, cos3)), columns=['quotes', 'authors', 'cos1', 'cos2', 'cos3'])

    sumed_cos_list = []

    for cos1_item, cos2_item, cos3_item in zip(cos1, cos2, cos3):

        sumed_cos = round((cos1_item + cos3_item)/2, 2)
        sumed_cos_list.append(sumed_cos)

    quotes_all['sum_cos'] =  sumed_cos_list

    quotes_all_sorted = quotes_all.sort_values(by=['sum_cos'], ascending=False)

    quotes_all_sorted_top_N = list(zip(quotes_all_sorted[:get_top_N_quotes]['sum_cos'], quotes_all_sorted[:get_top_N_quotes]['quotes'],
             quotes_all_sorted[:get_top_N_quotes]['authors']))

    quotes_all_sorted_top_N = [list(tup) for tup in quotes_all_sorted_top_N]

    return quotes_all_sorted_top_N



def format_quotes(base_lines_used_dict, user_query):

    formated_quotes_frame = format_to_frame(base_lines_used_dict, user_query)
    formated_quotes_dict = format_to_dict(formated_quotes_frame, user_query)

    return formated_quotes_frame, formated_quotes_dict


def main_run(user_query):

    args = get_default_args()

    # ToDo: Remove Time Setup once tested
    start_time = time.time()

    print('--- Get directories paths')
    output_dir, axilliary_dir, quotes_dir, embedding_file = get_folders_paths(args.embedding_file)

    print('--- Read pretrained embedding files')

    # print('------ Beginning to Read Embedding File -----')
    # emb_dict = read_json(os.path.join(axilliary_dir, embedding_file))
    # print('------ Done Reading Embedding File -----')
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    #
    print('------ Beginning to Read HMQ FILE -------')
    hmq_word_idf_dict = read_json(os.path.join(output_dir, 'hmq_word_idf_dict'))
    print('------ Done Reading HMQ File -----')
    #print("--- %s seconds ---" % (time.time() - start_time))
    #
    # stop_words = read_lines(os.path.join(axilliary_dir, 'custom_stopwords'))
    #
    # print('--- Clean user quote')
    # dp = DataProcessing()
    # processed_user_query = dp.sentence_cleaning(user_query)
    #
    # print('--- Compute query embedding')

    gec = GatheringEmbeddingsClass(user_query=user_query)

    user_query_emb = gec.sentence_embedding(hmq_word_idf_dict)

    # print('NEW EMBEDDINGS', user_query_emb )

    # ge = GetEmbeddings(emb_dict)
    # vocab = list(emb_dict.keys())
    #
    #
    #
    # user_query_emb = ge.sentence_embedding(dp, processed_user_query, vocab, emb_dict, hmq_word_idf_dict, stop_words)
    # print('OLD EMBEDDINGS', user_query_emb)
    print('--- Compute the closest embeddings')
    base_lines_used_dict = run_all_chosen_methods(args, output_dir, user_query_emb, user_query)

    print('--- Combine & Format Retrieved Quotes')
    formated_quotes_frame, formated_quotes_dict = format_quotes(base_lines_used_dict, user_query)

    print('--- Display the output')
    print_out(user_query, formated_quotes_frame)

    return formated_quotes_frame, formated_quotes_dict


def print_out(user_query, formated_quotes_frame):

    print('')
    print('*****************************************************')
    print('')
    print('User Query: ', user_query)
    print('')

    with pd.option_context('display.width', 5000, 'display.max_columns', 1000, 'display.expand_frame_repr', False,
                           'display.max_colwidth', -1):
        print('')
        print()
        short_formated_quotes_frame = formated_quotes_frame[['quote', 'author']]
        print(short_formated_quotes_frame)




if __name__ == "__main__":

    args = parser.parse_args()

    main_run(args.user_query)
