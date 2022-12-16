import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data2/hospital_review_final.csv')
df.info()
print(df.head())

df_stopwords = pd.read_csv('./stopwords.csv', index_col=0)
# 의미 없는 단어 추가로 제거 가능(주인공, 나라 이름 등)
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['받다', '치료', '비용', '전체', '지출', '원', '의원', '병원', '영수증', '인증', '방문', '예약', '게시', '진료', '약', '처방',
            '선생', '선생님', '원장', '원장님', '의사', '년', '월', '일', '신고', '하다', '하기', '도움', '가격', '정보', '미보험', '항목', '소독', '되어다']
df_stopwords2 = pd.DataFrame(stopwords, columns=['stopword'])

okt = Okt()
df['clean_reviews'] = None
count = 0

for idx, review in enumerate(df.reviews):
    count += 1
    if count % 10 == 0:
        print('.', end='')
    if count % 1000 == 0:
        print()
    review = re.sub('[^가-힣 ]', ' ', review)
    df.loc[idx, 'clean_reviews'] = review
    token = okt.pos(review, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_token = df_token[(df_token['class']=='Noun') |
                        (df_token['class']=='Verb') |
                        (df_token['class']=='Adjective')]
    # 불용어 제거
    words = []
    for word in df_token.word:
        if len(word) > 1:
            if word not in list(df_stopwords2.stopword):
                words.append(word)
    cleaned_sentence = ' '.join(words)
    df.loc[idx, 'clean_reviews'] = cleaned_sentence
print(df.head(30))
df.dropna(inplace=True)
df.to_csv('./crawling_data2/hospital_cleaned_reviews_final.csv', index=False)
