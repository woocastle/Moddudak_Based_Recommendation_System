# 자연어 처리할 때 가장 유용한 시각화 도구 = 워드클라우드
# 형태소 시각화 해봐야 => job09
# 잡8에서 먼저 뽑고 잡9에서 확인하는 식

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud     # pip install wordcloud
import collections
from matplotlib import font_manager, rc
from PIL import Image              # 그림 그려야하니
import matplotlib as mpl

# 잡6에서 가져온 부분 : 한글쓰기 위해
font_path = './malgun.ttf'     # 폰트 필요
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)    # 플랏에 한글 쓰려고 하는 것 안깨지고

df = pd.read_csv('./crawling_data2/one_sentences.csv')
words = df[df['hospitals']=='사랑이아프니치과의원']['reviews']  # 여기서 영화타이틀 바꾸면서 wordcloud 볼 수 있.
            # => 어떤 형태소 때문에 추천되었는지 알 수 있음
            # df의 타이틀스 (==' ')인 영화의 리뷰스를 가져와서 프린트
            # 난폭한 기록 (Fist & Furious)
print(words.iloc[0])                # 0번으로 출력
words = words.iloc[0].split()
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

# 컬렉션의 카운터를 이용하여 몇번나왔는지 출현빈도
# sort 해보면 되는데 더 편한 그래프(클라우드)로 볼 것
wordcloud_img = WordCloud(background_color='white', max_words=1500,       # 이미지출력 = 워드 클라우드     # 그림안에 출력되는 단어의 개수는 2000개로 제한
                          font_path=font_path).generate_from_frequencies(worddict)
plt.figure(figsize=(8, 8))
plt.imshow(wordcloud_img, interpolation='bilinear')                       # interpolation='bilinear' 삭제해도됨 (뒷글씨 블러처리)
plt.axis('off')
plt.show()

# # 한번에 클라우드 그림 2개 띄우기 위해 한번 더
# words = df[df['titles']=='겨울왕국 2 (Frozen 2)']['reviews']
# words = words.iloc[0].split()
# worddict = collections.Counter(words)
# worddict = dict(worddict)
# wordcloud_img = WordCloud(background_color='white', max_words=2000,
#                           font_path=font_path).generate_from_frequencies(worddict)
# plt.figure(figsize=(12, 12))
# plt.imshow(wordcloud_img, interpolation='bilinear')
# plt.axis('off')
# plt.show()

