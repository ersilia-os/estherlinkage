import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit


COLUMNS = ["src_idx", "trg_idx"]


class Split(object):

    def __init__(self, train_size):
        self.train_size = train_size
        self.splits = StratifiedShuffleSplit(n_splits=1, train_size=self.train_size)

    def _binarize(self, pairs, truth):
        src_set = set()
        truth_set = set()
        for r in truth[COLUMNS].values:
            truth_set.update([(r[0], r[1])])
            src_set.update([r[0]])
        R = []
        for r in pairs[COLUMNS].values:
            if r[0] in src_set:
                if (r[0], r[1]) in truth_set:
                    R += [1]
                else:
                    R += [0]
            else:
                R += [-1]
        return np.array(R, dtype=np.int)

    def _split(self, y):
        idxs = []
        test_idx = []
        for i, v in enumerate(y):
            if v == -1:
                test_idx += [i]
            else:
                idxs += [i]
        y_ = [y[i] for i in idxs]
        for train_idx, valid_idx in self.splits.split(y_, y_):
            pass
        train_idx = [idxs[i] for i in train_idx]
        valid_idx = [idxs[i] for i in valid_idx]
        train_idx = np.array(train_idx, dtype=np.int)
        valid_idx = np.array(valid_idx, dtype=np.int)
        test_idx = np.array(test_idx, dtype=np.int)
        return train_idx, valid_idx, test_idx

    def split(self, features, truth):
        pairs = features.index
        pairs = pd.DataFrame(np.array(pairs.to_frame(), dtype=np.int), columns=COLUMNS)
        y = self._binarize(pairs, truth)
        train_idx, valid_idx, test_idx = self._split(y)
        result = {
            "pairs": np.array(pairs, dtype=np.int),
            "y": y,
            "X": np.array(features),
            "train_idx": train_idx,
            "valid_idx": valid_idx,
            "test_idx": test_idx
        }
        return result
