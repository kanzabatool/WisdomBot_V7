# Import the Libraries
import re
from nltk.stem.porter import PorterStemmer
import pandas as pd

from lib.helpers.utils import remove_rows_with_nan_in_col

class DataProcessing():

    def __init__(self):
        pass


    def cleaning_data(self, dataset, col_name, remove_nan = False):
        '''
        
        :param dataset:
        :return:
        '''

        if remove_nan:
           dataset = remove_rows_with_nan_in_col(dataset, col_name)

        processed_sent_list = []

        quotes_list = list(dataset[col_name])

        for quote in quotes_list:
            processed_sen = self.sentence_cleaning(quote)
            processed_sent_list.append(processed_sen)

        processed_col_name = 'processed_' + col_name
        dataset[processed_col_name] = processed_sent_list

        dataset = remove_rows_with_nan_in_col(dataset, col_name)

        return dataset


    def sentence_cleaning(self, sentence):

        '''
        Cleans the sentence by lower casing it and removing punctuations
        :param sentence:
        :return:
        '''

        processed_sen = re.sub('[^a-zA-Z]', ' ', sentence)
        processed_sen = processed_sen.lower()
        processed_sen = self.tokenize_sentence(processed_sen)
        ps = PorterStemmer()
        #processed_sen = [ps.stem(word) for word in processed_sen if not word in set(stopwords.words('english'))]
        #processed_sen_no_stopword = [word for word in processed_sen if not word in set(stopwords.words('english'))]

        return ' '.join(processed_sen)


    def tokenize_sentence(self, sentence):

        processed_sen = re.findall(r"[\w']+|[.,!?;]", sentence)

        return processed_sen



    def remove_starting_trailing_spaces(self, my_string):

        my_string = my_string.strip()

        return my_string



    def format_hm_queries(self, quotes_df, quotes_col_name, hmq_col_name, authors_col_name, remove_nan):

        if remove_nan:
            dataset = remove_rows_with_nan_in_col(quotes_df, hmq_col_name)

        formatted_hmq_sent_list = []
        rep_quotes_col_list = []
        rep_author_col_list = []
        rep_id_col_list = []

        id_col_list = list(dataset['id'])
        hmq_col_list = list(dataset[hmq_col_name])
        quotes_col_list = list(dataset[quotes_col_name])
        authors_col_list = list(dataset[authors_col_name])

        for quote, hm_string, author, id in zip(quotes_col_list, hmq_col_list, authors_col_list, id_col_list):

            hm_queries = hm_string.split('||')

            num_of_questions = len(hm_queries)
            quote_rep = [quote] * num_of_questions
            author_rep = [author] * num_of_questions
            id_rep     = [id] * num_of_questions

            formatted_hmq_sent_list = formatted_hmq_sent_list + hm_queries
            rep_author_col_list = rep_author_col_list + author_rep
            rep_quotes_col_list = rep_quotes_col_list + quote_rep
            rep_id_col_list     = rep_id_col_list     + id_rep


        formated_hmq_frame = pd.DataFrame({'id': rep_id_col_list, 'Author': rep_author_col_list,'Quotes': rep_quotes_col_list, 'Queries': formatted_hmq_sent_list})

        return formated_hmq_frame





