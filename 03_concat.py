import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/*')
df = pd.DataFrame()
for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
print(len(df.hospitals.value_counts()))
df.to_csv('./crawling_data2/hospital_review_final.csv', index=False)