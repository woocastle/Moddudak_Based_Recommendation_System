import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    hospital_idx = [i[0] for i in simScore]
    rechospital = df_reviews.iloc[hospital_idx, 0]
    return rechospital

df_reviews = pd.read_csv('./crawling_data2/one_sentences.csv')
tfidf_matrix = mmread('./models/tfidf_hospital_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    tfidf = pickle.load(f)

# # 병원 이용
# hospital_idx = df_reviews[df_reviews['hospitals']=='사과나무치과병원'].index[0]
# cosin_sim = linear_kernel(tfidf_matrix[hospital_idx], tfidf_matrix)
# print(cosin_sim)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation[1:11])

# #키워드 활용
# embedding_model = Word2Vec.load('./models/word2vec_hospital_review.model')
# key_word = '임플란트'
# sim_word = embedding_model.wv.most_similar(key_word, topn=10)
# words = [key_word]
# for word, _ in sim_word:
#     words.append(word)
# print(words)
# sentence = []
# count = 11
# for word in words:
#     sentence = sentence + [word] * count
#     count -= 1
# sentence = ' '.join(sentence)
# print(sentence)
# sentence_vec = tfidf.transform([sentence])
# cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation)

#문장 활용
sentence = '이빨이 아파요'
review = re.sub('[^가-힣 ]', ' ', sentence)
okt = Okt()
token = okt.pos(review, stem=True)
df_token = pd.DataFrame(token, columns=['word', 'class'])
df_token = df_token[(df_token['class']=='Noun') |
                    (df_token['class']=='Verb') |
                    (df_token['class']=='Adjective')]
words = []
for word in df_token.word:
    if 1 < len(word):
        words.append(word)
cleaned_sentence = ' '.join(words)
print(cleaned_sentence)
sentence_vec = tfidf.transform([cleaned_sentence])
cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
recommendation = getRecommendation(cosin_sim)
print(recommendation)










