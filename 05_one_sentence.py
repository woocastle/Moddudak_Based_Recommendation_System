import pandas as pd

df = pd.read_csv('./crawling_data2/hospital_cleaned_reviews_final.csv')
df.dropna(inplace=True)
df.info()
one_sentences = []
for hospital in df['hospitals'].unique():
    temp = df[df['hospitals']==hospital]
    if len(temp) > 30:
        temp = temp.iloc[:30, :]
    one_sentence = ' '.join(temp['clean_reviews'])
    one_sentences.append(one_sentence)
df_one = pd.DataFrame({'hospitals':df['hospitals'].unique(), 'reviews':one_sentences})
print(df_one.head())
df_one.to_csv('./crawling_data2/one_sentences.csv', index=False)