import pandas as pd


class WaterfallFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def preprocess(self):
        df = pd.read_csv(self.filepath, sep=";")
        df['norm_text'] = df.summary.map(lambda x: x.replace('«', ' '))
        df['norm_text'] = df.norm_text.map(lambda x: x.replace('»', ' '))
        df['norm_text'] = df.norm_text.map(lambda x: x.replace('/', ' '))
        df['norm_text'] = df.norm_text.map(lambda x: x.replace(',', ' '))
        df['norm_text'] = df.norm_text.map(lambda x: x.replace(':', ' '))
        df['norm_text'] = df.norm_text.map(lambda x: x.replace('  ', ' '))
        df = df.drop_duplicates(subset=['norm_text'], keep=False)
        waterfalls = pd.DataFrame(
            df.norm_text.str.split('\n').tolist(),
            index=df.title).stack()
        waterfalls = waterfalls.reset_index([0, 'title'])
        waterfalls.columns = ['title', 'norm_text']
        return waterfalls
