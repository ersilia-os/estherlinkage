import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

MAX_FEATURES = 200
NGRAM_RANGE = (2, 2)


class Block(object):

    def __init__(self, df, columns, k):
        self.k = k
        self.mdl = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=NGRAM_RANGE,
            max_features=MAX_FEATURES
        )
        self.nn = NearestNeighbors(
            n_neighbors=self.k
        )
        self._index(df, columns)

    def _concat(self, df, columns):
        R = []
        for v in df[columns].values:
            r = []
            for x in v:
                if str(x) == "nan":
                    continue
                r += [str(x).lower()]
            R += [" ".join(r)]
        return R

    def _fit_vectorize(self, data):
        self.mdl.fit(data)

    def _fit_nearest_neighbors(self, data):
        V = self.mdl.transform(data).toarray()
        self.nn.fit(V)

    def _get_nearest_neighbors(self, data):
        V = self.mdl.transform(data).toarray()
        _, indices = self.nn.kneighbors(V)
        return indices

    def _index(self, df, columns):
        data = self._concat(df, columns)
        self._fit_vectorize(data)
        self._fit_nearest_neighbors(data)

    def block(self, df, columns):
        data = self._concat(df, columns)
        indices = self._get_nearest_neighbors(data)
        R = []
        for i in range(len(indices)):
            for v in indices[i]:
                R += [(i, v)]
        pairs = pd.DataFrame(R, columns=["src_idx", "trg_idx"])
        return pd.MultiIndex.from_frame(pairs)
