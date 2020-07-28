import json

with open("full_conceptnet_dict.txt", 'r') as json_data:
    data = json.load(json_data)
    

chunk = ["al", "an","ar","ba","be", "bi" ,"bl" ,"bo" ,"br" ,"bu",
         "ca","ch", "cl", "co","cr","de","di","do","ma", "me", "mi" ,"mo", "mu","my",
        "pa","pe", "ph","pi", "pl","po","pr","sa", "sc", "se", "sh", "si", "so","sp", "st","su"]
singles = ['e','f','g','h','i','j','k','l','n','o','q','r','t','u','v','w','x','y','z']
    

def split(x):
    x = {key:val for key, val in data.items()  
                   if key.startswith(x)}
    return(x)

A = split('a')
B = split('b')
C = split('c')
D = split('d')
M = split('m')
P = split('p')
S = split('s')
    
for v in chunk:
    with open("split/sub-file"+str(v.upper()), "w") as fp: 
                json.dump(split(v), fp) 
            
for v in singles:
    with open("split/file-"+str(v.upper()), "w") as fp: 
                json.dump(split(v), fp) 
            
for key in list(A.keys()): 
    if key.startswith(("al", "an","ar")): 
            A.pop(key)
with open("split/sub-fileA", "w") as fp: 
    json.dump(A, fp)
    
for key in list(B.keys()): 
    if key.startswith(("ba","be", "bi" ,"bl" ,"bo" ,"br" ,"bu")): 
            B.pop(key)
with open("split/sub-fileB", "w") as fp: 
    json.dump(B, fp)
    

for key in list(D.keys()): 
    if key.startswith(("de","di","do")): 
            D.pop(key)
with open("split/sub-fileD", "w") as fp: 
    json.dump(D, fp)
    
    
for key in list(M.keys()): 
    if key.startswith(("ma", "me", "mi" ,"mo", "mu","my")): 
            M.pop(key)
with open("split/sub-fileM", "w") as fp: 
    json.dump(M, fp)
    
    
for key in list(P.keys()): 
    if key.startswith(("pa","pe", "ph","pi", "pl","po","pr")): 
            P.pop(key)
with open("split/sub-fileP", "w") as fp: 
    json.dump(P, fp)
    

for key in list(S.keys()): 
    if key.startswith(("sa", "sc", "se", "sh", "si", "so","sp", "st","su")): 
            S.pop(key)
with open("split/sub-fileS", "w") as fp: 
    json.dump(S, fp) 
    
for key in list(C.keys()): 
    if key.startswith(("ca","ch", "cl")): 
            C.pop(key)
with open("split/sub-fileC", "w") as fp: 
    json.dump(C, fp)
    
    
    
#custom words

custom_words = ["i","me","my","myself","you","your","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"]


stop_words = {k: data[k] for k in set(custom_words) & set(data.keys())}

with open("split/CustomWords", "w") as fp: 
    json.dump(stop_words, fp)