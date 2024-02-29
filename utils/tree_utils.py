import bigtree as bt

def create_path_from_record(r):
    res = ""
    for val in r:
        res = f"{val}/" + res
    return res[:-1]

def tree_fromdf(df):
    path_lst =  df.aggregate(create_path_from_record, axis='columns').tolist()
    return bt.list_to_tree(path_lst)
