import pandas as pd

from lib.helpers.utils import get_nth_item_nested_list, sort_dataframe, remove_duplicates_df_col



def format_to_frame(base_lines_used_dict, user_query):

    names_of_baselines = list(base_lines_used_dict.keys())

    all_quotes_list = []

    similarities_list = []
    quotes_list = []
    authors_list = []
    keywords_list = []
    queries_list = []
    baselines_list = []
    ids_list = []

    for baseline in names_of_baselines:

        quotes_info = base_lines_used_dict[baseline]

        similarities = get_nth_item_nested_list(quotes_info, 0)
        quotes = get_nth_item_nested_list(quotes_info, 1)
        authors = get_nth_item_nested_list(quotes_info, 2)
        ids     = get_nth_item_nested_list(quotes_info, len(quotes_info[0])-1)
        keywords = ['-'] * len(quotes)
        queries = ['-'] * len(quotes)
        method_list = [baseline] * len(quotes)

        if baseline == 'keywords':
            keywords = get_nth_item_nested_list(quotes_info, 3)

        if baseline == 'queries':
            queries = get_nth_item_nested_list(quotes_info, 3)

        similarities_list = similarities_list + similarities
        quotes_list = quotes_list + quotes
        keywords_list = keywords_list + keywords
        queries_list = queries_list + queries
        baselines_list = baselines_list + method_list
        authors_list = authors_list + authors
        ids_list = ids_list + ids

    all_top_quotes_frame =  pd.DataFrame({'id':ids_list, 'similarity': similarities_list, 'quote': quotes_list, 'author': authors_list, 'method': baselines_list, 'keywords': keywords_list, 'query': queries_list})
    all_top_quotes_frame = sort_dataframe(all_top_quotes_frame, 'similarity')

    all_top_quotes_frame['user_query'] = [user_query] * all_top_quotes_frame.shape[0]

    all_top_quotes_frame = all_top_quotes_frame[['user_query', 'similarity', 'quote', 'author', 'method', 'keywords',  'query', 'id']]

    all_top_quotes_frame = remove_duplicates_df_col(all_top_quotes_frame, 'quote')

    return all_top_quotes_frame


def format_to_dict(all_top_quotes_frame, user_query):

    formated_quotes_dict = {}
    formated_quotes_dict[user_query] = {}

    names_of_baselines = list(set(list(all_top_quotes_frame['method'])))

    for index, row in all_top_quotes_frame.iterrows():

        quote      = row['quote']
        author     = row['author']
        similarity = row['similarity']
        method     = row['method']
        query      = row['query']
        keywords   = row['keywords']
        id         = row['id']

        formated_quotes_dict[user_query][id] =  {}

        quotes_info_dict = {}
        quotes_info_dict['quote'] = quote
        quotes_info_dict['author'] = author
        quotes_info_dict['similarity'] = similarity
        quotes_info_dict['method'] = method
        quotes_info_dict['label'] = '-'

        if method == 'keywords':
            quotes_info_dict['keywords'] = {}
            quotes_info_dict['keywords'] = keywords

        if method == 'queries':
            quotes_info_dict['queries'] = {}
            quotes_info_dict['queries'] = query

        formated_quotes_dict[user_query][id] = quotes_info_dict

    return formated_quotes_dict

