import os
import pandas as pd
import numpy as np

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 60)

df_original = pd.read_pickle('whole_set_selected2.pkl')
df_original2 = pd.read_pickle('whole_set_selected2.pkl')

df_original = df_original.reset_index()

df_original = df_original[df_original['reserved_for_calibration']==False]
df_original = df_original[np.logical_or(df_original['drowsiness']==1, df_original['drowsiness']==0)]


df = df_original.loc[df_original['face_detected'] == 1]
df_original2 = df_original.loc[df_original['face_detected'] == 1]


user_list = list(df['subject'].unique())


list_of_all_original=[]
for user in user_list:
    list_of_all_original.append(df.groupby('subject').get_group(user))

df_nonsleepycombination_and_mix = df[df['facial_actions'].isin(['nonsleepyCombination','mix'])]


list_of_all_groups = []
for user in user_list:
    list_of_all_groups.append(df_nonsleepycombination_and_mix.groupby('subject').get_group(user))


list_of_all_first_90 = []
for user in user_list:
    list_of_all_first_90.append(df_nonsleepycombination_and_mix.groupby('subject').get_group(user)[:90])


##### standart scaler çalıştırma
from sklearn.preprocessing import StandardScaler

lastest_df_list=[]
for i in range(len(list_of_all_first_90)):
    scaler = StandardScaler()
    scaler.fit(list_of_all_first_90[i].loc[ : , ["left_ear", "right_ear", "avg_ear", 
                                              "mar", "moe", "left_eye_circularity", 
                                              "right_eye_circularity","avg_eye_circularity", "left_leb", "right_leb", 
                                              "avg_leb","left_sop", "right_sop", "avg_sop"]])
    last_df =pd.DataFrame(scaler.transform(list_of_all_original[i].loc[ : , ["left_ear", "right_ear", "avg_ear", 
                                              "mar", "moe", "left_eye_circularity", 
                                              "right_eye_circularity","avg_eye_circularity", "left_leb", "right_leb", 
                                              "avg_leb","left_sop", "right_sop", "avg_sop"]]))
    
    
    
    last_df.columns=["n_left_ear", "n_right_ear", "n_avg_ear", 
                    "n_mar", "n_moe", "n_left_eye_circularity", 
                    "n_right_eye_circularity","n_avg_eye_circularity", "n_left_leb", "n_right_leb", 
                    "n_avg_leb","n_left_sop", "n_right_sop", "n_avg_sop"]
    
    
    last_df['subject']=user_list[i]
    lastest_df_list.append(last_df)


    
df_merged = pd.concat(lastest_df_list)
lastList = []


for col in df_merged.columns:
    df_original2[col] = ""
    columns_orderly = df_merged[col]
    columns_orderly.index = df_original2.index
    df_original2[col] = columns_orderly


df_original2.to_pickle("one_eye_with_still_problem.pkl")



