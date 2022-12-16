import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
import pandas as pd
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import linear_kernel
import re
from konlpy.tag import Okt

form_window = uic.loadUiType('./modudak_recommendation_app.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 모델들 불러오기
        self.setWindowTitle('Modoodoc')
        self.tfidf_matrix = mmread('./models/tfidf_hospital_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_hospital_review.model')

        # 콤보 박스에 추가!
        self.df_reviews = pd.read_csv('./crawling_data2/one_sentences.csv')
        self.hospitals = self.df_reviews['hospitals']
        self.hospitals = sorted(self.hospitals)

        # 버튼을 눌러 라벨상자에 출력
        self.btn_recommend.clicked.connect(self.btn_slot)

    # 병명으로 추천 (단어)
    def recommendation_by_key_word(self, key_word):
        sim_word = self.embedding_model.wv.most_similar(key_word, topn=10)
        words = [key_word]
        for word, _ in sim_word:
            words.append(word)
        print(words)
        sentence = []
        count = 19
        for word in words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        print(sentence)
        sentence_vec = self.tfidf.transform([sentence])
        cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)

        # 링크 연결
        link = []
        for i in range(1, 11):
            link.append('{}.<a href="https://www.modoodoc.com/hospitals/?search_query={}">{}</a><br>'.format(i, list(recommendation)[i - 1], list(recommendation)[i - 1]))
        link = '\n'.join(link)
        self.lbl_recommend.setText(link)
        self.lbl_recommend.setOpenExternalLinks(True)

    # 증상으로 추천 (문장)
    def recommendation_by_sentence(self, key_word):
        review = re.sub('[^가-힣 ]', ' ', key_word)
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
        sentence_vec = self.tfidf.transform([cleaned_sentence])
        cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)

        # 링크 연결
        link = []
        for i in range(1, 11):
            link.append('{}.<a href="https://www.modoodoc.com/hospitals/?search_query={}">{}</a><br>'.format(i, list(recommendation)[i - 1], list(recommendation)[i - 1]))
        link = '\n'.join(link)
        self.lbl_recommend.setText(link)
        self.lbl_recommend.setOpenExternalLinks(True)

    def btn_slot(self):
        key_word = self.line_edit.text()
        if key_word in list(self.embedding_model.wv.index_to_key):
            self.recommendation_by_key_word(key_word)
        else:
            self.recommendation_by_sentence(key_word)

    def getRecommendation(self, cosin_sim):
        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        hospital_idx = [i[0] for i in simScore]
        print(len(hospital_idx))
        rechospitalList = self.df_reviews.iloc[hospital_idx, 0]
        print(rechospitalList)
        return rechospitalList

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
