##A version without saving the data chunks.
import pandas as pd
import os
from functools import reduce
from collections import Counter

def get_n_common_errors(logs_path,n):
    def get_df(path):
        return pd.read_excel(path, engine="openpyxl", header=None)

    def divide_df(path,chunk_size):
        """return a list of the chunks pathes"""
        counters=[]
        df=get_df(path)

        for i,start in enumerate(range(0,len(df),chunk_size)):
            df_chunk=df.iloc[start:start+chunk_size]
            curr_counter=df_chunk[0].value_counts()
            counters.append(curr_counter)
        return counters


    def add_counts(counts_list):
        return (reduce(lambda x,y:x.add(y,fill_value=0),counts_list))

    def get_n_common(count_fre,n):
        counter_fre=Counter(count_fre.to_dict())
        return counter_fre.most_common(n)

    DATA_CHUNK=10**5
    count_list=divide_df(logs_path,DATA_CHUNK)
    total_count=add_counts(count_list)
    return get_n_common(total_count,n)


#MAIN
logs_path=r"C:\Users\The user\Documents\לימודי מחשבים\שנה ג\סמסטר ב\הדסים\HomeworkProject\logs.txt.xlsx"
DESIRED_LINES=3
print(get_n_common_errors(logs_path,DESIRED_LINES))

#----------Analysis of time and space complexity------------

#Let's call the size of the given file N

#------Time complexity:-----
#O(N)
#Reason: Each of the operations on the file is O(N) , so the order of magnitude of the connection of all operations is also linear

#------Space complexity--------
#0(K) Where k is the required data chunk size
#Reason: We only analyze a piece of information of size K at a time.