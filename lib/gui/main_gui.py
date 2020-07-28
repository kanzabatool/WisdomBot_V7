#======================MISCELLANEOUS================================

import sys
import pandas as pd
from pathlib import Path

parent_dir = str(Path(__file__).parents[2])
sys.path.insert(0, parent_dir)

from lib.gui.gui_class import GUI
from lib.retrievers.main_retrieve_top_quote import main_run

# GUI
gu = GUI()

#========================MAIN CODE=================================



# Input: User query
user_query = "Who are you?"

# Bot's think process
formated_quotes_frame, formated_quotes_dict = main_run(user_query)

# Bot's Response
output_bot_response = formated_quotes_frame['quote'][0]
output_author = formated_quotes_frame['author'][0]

print('You      : ', user_query)
print('')
print('WisdomBot: ', output_bot_response)

# Get User's Feedback
user_score = gu.gui_input('User             : {} \n\nWisdomBot  : {} \n\n\nthumbs up? 1=Yes, 0=No'.format(user_query, output_bot_response))

label_frame = pd.DataFrame([user_score] + ['-'] * (formated_quotes_frame.shape[0] - 1), columns = ['label'])
formated_quotes_frame = pd.concat([formated_quotes_frame, label_frame], axis=1)

# Save user query and bot's response
gu.save_feedback(formated_quotes_frame)




