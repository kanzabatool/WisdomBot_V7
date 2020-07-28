# Import the Libraries
from lib.helpers.utils import write_json


emb_dict={}
with open('/Users/bhaider/Documents/Dreams/WisdomBot/Wisdom_Bot/wbh_axilliary_data/numberbatch-en-19.08.txt','r') as f:
    for line in f:
        data=line.split()
        emb_vec_string = list(data[1:])
        emb_vec = [float(item) for item in emb_vec_string]
        emb_dict[data[0]]=  emb_vec

write_json(emb_dict, '/Users/bhaider/Documents/Dreams/WisdomBot/Wisdom_Bot/wbh_axilliary_data/full_conceptnet_dict.txt')