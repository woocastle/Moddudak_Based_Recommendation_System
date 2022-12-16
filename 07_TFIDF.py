import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer     # 벡터들을 행렬로 저장
from scipy.io import mmwrite, mmread            # 행렬을 쓰고 읽어준다.
import pickle

df_reviews = pd.read_csv('./crawling_data2/one_sentences.csv')
df_reviews.info()

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df_reviews['reviews'])
print(tfidf_matrix[0].shape)
with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(tfidf, f)
mmwrite('./models/tfidf_hospital_review.mtx', tfidf_matrix)










