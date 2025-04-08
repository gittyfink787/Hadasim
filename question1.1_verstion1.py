#A version for saving the data chunks for using in the future
import pandas as pd
import os
from functools import reduce
from collections import Counter

def get_n_common_errors(logs_path,n):
    def get_df(path):
        return pd.read_excel(path, engine="openpyxl", header=None)

    def divide_df(path,chunk_size):
        """return a list of the chunks pathes"""
        pathes=[]
        df=get_df(path)

        for i,start in enumerate(range(0,len(df),chunk_size)):
            df_chunk=df.iloc[start:start+chunk_size]

            output_dir = "process_data_1"
            os.makedirs(output_dir, exist_ok=True)
            file_name=f"part_{i+1}_logs.xlsx"
            file_path=os.path.join(r"C:\Users\The user\Documents\לימודי מחשבים\שנה ג\סמסטר ב\הדסים\HomeworkProject\process_data_1",file_name)

            df_chunk.to_excel(file_path,index=False,header=False,engine="openpyxl")
            pathes.append(file_path)

        return pathes

    def count_values_from_path(path):
        df=get_df(path)
        counts=df[0].value_counts()
        return counts

    def count_values_from_list_of_pathes(pathes):
        counts_list=[]
        for path in pathes:
            counts_list.append(count_values_from_path(path))
        return counts_list

    def add_counts(counts_list):
        return (reduce(lambda x,y:x.add(y,fill_value=0),counts_list))

    def get_n_common(count_fre,n):
        counter_fre=Counter(count_fre.to_dict())
        return counter_fre.most_common(n)

    DATA_CHUNK=10**5
    pathes=divide_df(logs_path,DATA_CHUNK)
    count_list=count_values_from_list_of_pathes(pathes)
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
#Note: The relatively high running time is due to the large number of input and output operations in the program, below is an improved version

#------Space complexity--------
#0(N)
#Reason: We saved each given record once, so the complexity is linear in the input size


