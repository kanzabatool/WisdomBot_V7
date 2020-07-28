# Import the Libraries
import tkinter as tk
from tkinter import simpledialog
import os

from lib.helpers.utils import get_parent_folder, get_file_path_in_cwd


class GUI():

    def __init__(self):
        pass

    # Ask for user input with GUI
    def gui_input(self, my_prompt):
        '''
        User input in GUI
        :param takes user input
        :return: user input
        '''
        ROOT = tk.Tk()
        ROOT.withdraw()
        USER_INP = simpledialog.askstring(title="Ancient Wisdom",
                                          prompt=my_prompt)
        return USER_INP

    # Saving user feeback
    #def save_feedback(self, user_query, top_quote_author, top_quote, user_feedback, use_bow_simple_avg_quotes, use_bow_simple_avg_hm_queries):
    def save_feedback(self, formated_quotes_frame):

        formated_quotes_frame = formated_quotes_frame.iloc[[0]]

        cwd_file = get_file_path_in_cwd('gui_class.py')
        parent_dir = get_parent_folder(cwd_file)
        #feedback_file = os.path.dirname(os.path.join(parent_dir, 'data','output','dictionaries')) + '/user_feedback'
        feedback_dir = os.path.dirname(os.path.join(parent_dir, 'data', 'output', 'dictionaries'))
        feedback_file = os.path.join(os.path.join(feedback_dir, 'user_feedback'))

        if os.path.exists(feedback_file):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not

        if append_write== 'a':
            formated_quotes_frame.to_csv(feedback_file, mode=append_write, header=None, sep='\t', index=False)
        else:
            formated_quotes_frame.to_csv(feedback_file, mode=append_write, header=list(formated_quotes_frame), sep='\t', index=False)



