import numpy as np
import scipy
import fasttext
from nltk.corpus import stopwords
from service.fasttext.dataframe import WaterfallFile
from pathlib import Path


class FasttextModel():
    model_path = Path('service') / 'fasttext' / 'wiki.ru.bin'
    csv_path = Path('service') / 'fasttext' / 'waterfalls_fasttext.csv'

    fasttext_model = fasttext.load_model('service/fasttext/wiki.ru.bin')

    def cos_similarity(self, data1, data2):
        stop = stopwords.words('russian')
        sent1_emb = np.mean(
                                [
                                    FasttextModel().fasttext_model[x]
                                    for word in data1 for x in word.split()
                                    if x not in stop
                                ], axis=0
                            )
        sent2_emb = np.mean(
                                [
                                    FasttextModel().fasttext_model[x]
                                    for word in data2 for x in word.split()
                                    if x not in stop
                                ], axis=0
                            )
        if sent1_emb.all():
            return 1-scipy.spatial.distance.cosine(sent1_emb, sent2_emb)

    def predict_result(self, user_text):
        max_index = 0
        max_similarity = 0
        waterfall = WaterfallFile().preprocess(FasttextModel().csv_path)
        for index, row in waterfall.iterrows():
            if FasttextModel().cos_similarity(
                    row['norm_text'], user_text) > max_similarity:
                max_similarity = FasttextModel().cos_similarity(
                    row['norm_text'], user_text)
                max_index = index
        return waterfall.iloc[max_index]['title'], max_similarity
