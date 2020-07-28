# Import the Libraries
import os
import sys
import argparse
import warnings
from collections import defaultdict
from pathlib import Path
from timeit import default_timer as timer

parent_dir = str(Path(__file__).parents[2])
sys.path.insert(0, parent_dir)

from lib.helpers.utils import read_json, write_json, read_tsv, concatenate_list_df, read_lines
from lib.helpers.embedding_class import GetEmbeddings
from lib.helpers.preprocessing_class import DataProcessing


# For declaring and documenting the code
parser = argparse.ArgumentParser(description='Wisdom Bot')
parser.add_argument('--embedding_file', help='txt file containing embedding dictionary',
                    default='full_conceptnet_dict.txt')
#parser.add_argument('--list_of_quotes_files_to_emb', type=list, help='tsv file containing quotes', \
#                    default=['quotes.tsv'])
parser.add_argument('--list_of_quotes_files_to_emb', type=list, help='tsv file containing quotes', \
                    default=['quotes.tsv'])
parser.add_argument('--quotes_col_name', help='tsv file containing quotes', default='Quotes')
parser.add_argument('--human_queries_col_name', help='tsv file containing quotes', default='Queries')
parser.add_argument('--keywords_col_name', help='tsv file containing quotes', default='Key_Words')
parser.add_argument('--authors_col_name', help='tsv file containing quotes', default='Author')


# Ignore python warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


def read_quotes_data_list(quotes_data_folder, list_of_quotes_files_to_emb):

    quotes_df_list = []

    for quote_file_name in list_of_quotes_files_to_emb:

        quote_file_path = os.path.join(quotes_data_folder, quote_file_name)
        quote_df = read_tsv(quote_file_path)
        quotes_df_list.append(quote_df)

    return quotes_df_list


def get_quotes_emb_dict(quotes_df_processed, col_name_emb, quote_col_name, emb_dict, idf_dict, stop_words):

    ge = GetEmbeddings(emb_dict)

    required_emb_dict = defaultdict(str)

    ret_sent_list = quotes_df_processed[col_name_emb]
    processed_ret_sent_list = quotes_df_processed['processed_' + col_name_emb]
    author_list = quotes_df_processed['Author']
    quote_col_list = quotes_df_processed[quote_col_name]
    id_col_list = quotes_df_processed['id']

    sent_dict = ge.sentences_list_embedding(processed_ret_sent_list, ret_sent_list, author_list, quote_col_list, id_col_list, idf_dict, stop_words)

    return sent_dict


def get_folders_paths(embedding_file):

    main_folder_path = str(Path(__file__).parents[1])

    output_dir = os.path.join(main_folder_path, 'data','output','dictionaries')
    axilliary_dir = os.path.join(main_folder_path, 'data','axillary')
    quotes_dir = os.path.join(main_folder_path, 'data','quotes')

    embedding_file = os.path.join(axilliary_dir, embedding_file)

    return output_dir, axilliary_dir, quotes_dir, embedding_file


if __name__ == "__main__":

    start = timer()

    args = parser.parse_args()

    dp = DataProcessing()

    print('--- Get directories paths')
    output_dir, axilliary_dir, quotes_dir, embedding_file = get_folders_paths(args.embedding_file)

    print('--- Reading embeddings')
    emb_dict = read_json(os.path.join(axilliary_dir, embedding_file))
    #stop_words = read_lines(os.path.join(axilliary_dir, 'custom_stopwords'))
    stop_words = read_lines(os.path.join(axilliary_dir, 'nltk_stopwords'))

    print('--- Importing quotes datasets')
    quotes_df_list = read_quotes_data_list(quotes_dir, args.list_of_quotes_files_to_emb)

    print('--- Merging all quotes into a single dataframe')
    quotes_df = concatenate_list_df(quotes_df_list)
    hm_queries_quotes_df_formatted = dp.format_hm_queries(quotes_df, args.quotes_col_name, args.human_queries_col_name, args.authors_col_name, remove_nan=True)

    print('--- Data cleaning')
    quotes_df_processed = dp.cleaning_data(quotes_df, args.quotes_col_name, remove_nan = True)
    hm_queries_quotes_df_formatted = dp.cleaning_data(hm_queries_quotes_df_formatted, args.human_queries_col_name, remove_nan=True)
    keywords_df_processed = dp.cleaning_data(quotes_df, args.keywords_col_name, remove_nan=True)

    print('--- Compute IDF Scores')
    ge = GetEmbeddings(emb_dict)
    quotes_idf_dict = ge.compute_tf_idf(dp, list(set(quotes_df_processed['processed_Quotes'])))
    hm_queries_idf_dict = ge.compute_tf_idf(dp, list(set(hm_queries_quotes_df_formatted['processed_Queries'])))
    write_json(quotes_idf_dict, os.path.join(output_dir, 'quotes_word_idf_dict'))
    write_json(hm_queries_idf_dict, os.path.join(output_dir, 'hmq_word_idf_dict'))
    write_json({}, os.path.join(output_dir, 'keywords_emb_dict_idf_dict'))

    print('--- Get quotes embeddings dict')
    quotes_emb_dict     = get_quotes_emb_dict(quotes_df_processed, args.quotes_col_name, args.quotes_col_name, emb_dict, quotes_idf_dict, stop_words)
    hmq_quotes_emb_dict = get_quotes_emb_dict(hm_queries_quotes_df_formatted, args.human_queries_col_name, args.quotes_col_name, emb_dict, hm_queries_idf_dict, stop_words)
    keywords_emb_dict   = get_quotes_emb_dict(keywords_df_processed, args.keywords_col_name, args.quotes_col_name, emb_dict, {}, [])

    print('--- Save quotes embeddings dict')
    write_json(quotes_emb_dict, os.path.join(output_dir, 'quotes_emb_dict'))
    write_json(hmq_quotes_emb_dict, os.path.join(output_dir, 'hmq_quotes_emb_dict'))
    write_json(keywords_emb_dict, os.path.join(output_dir, 'keywords_quotes_emb_dict'))

    end = timer()

    end_time_min  = round((end - start) / 60, 2)
    end_time_hour = round((end - start) / 3600, 2)

    print('Inference time in minutes: {}'.format(end_time_min))
    print('Inference time in hours  : {}'.format(end_time_hour))