import pandas as pd
import json
import os

def read_json(file_path):
    '''
    Loads dictionary
    :param file_path: file containing the  dictionary
    :return: the dictionary
    '''
    my_dict = json.load(open(file_path))
    return my_dict

def write_json(data, file_path):
    '''
    Writes dictionary
    :param file_path: file containing the  dictionary
    :return: the dictionary
    '''
    with open(file_path, 'w') as f:
        json.dump(data, f)


def read_tsv(file_path):
    '''
    reads tsv and returns data frame
    :param file_path: file containing the dataframe
    :return: dataframe
    '''
    dataset = pd.read_csv(file_path, delimiter='\t', quoting=3,  encoding='utf-8')
    return dataset

def read_xlsx(file_path):
    '''
    reads xlsx and returns data frame
    :param file_path: file containing the dataframe
    :return: dataframe
    '''
    dataset = pd.read_excel(open(file_path,'rb'))
    return dataset


def write_tsv(file_name, df):
    '''
    reads tsv amd returns data frame
    :param file_path: file containing the dataframe
    :return: dataframe
    '''

    dataset = df.to_csv(file_name, sep='\t', encoding='utf-8')


def concatenate_list_df(df_list):

    df_big = pd.concat(df_list)

    return df_big

def remove_rows_with_nan_in_col(df, col_name):

    df = df[df[col_name].notna()]

    return df


def get_file_path_in_cwd(file_name):

    cwd_file = os.path.join(os.getcwd(), file_name)

    return cwd_file


def get_parent_folder(file_path):

   parent_dir = os.path.dirname(os.path.dirname(file_path))

   return parent_dir


def read_lines(file_path):

    with open(file_path) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    return content

def sort_dataframe(df, col_name):

    df.sort_values(col_name, inplace=True, ascending=False)

    return df

def get_nth_item_nested_list(l, n):

    nth_item = [el[n] for el in l]

    return nth_item

def remove_duplicates_df_col(df, col):

    df = df.drop_duplicates(subset=col, keep='first')

    df.reset_index(drop=True, inplace=True)

    return df


def remove_duplicates_nested_list(l, item_idx):
    seen = set()
    cond = [x for x in l if x[item_idx] not in seen and not seen.add(x[item_idx])]
    return cond

def remove_items_from_list_given_indices(my_list, idx_del_list):

    for index in sorted(idx_del_list, reverse=True):
        del my_list[index]

    return my_list

def split(a, n):
    #split list into n equal parts
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


if __name__ == "__main__":
    pass