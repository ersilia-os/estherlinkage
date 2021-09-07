import pandas as pd


class Assemble(object):

    def __init__(self, pairs, y, df_a, df_b):
        self.pairs = pairs[y == 1]
        self.df_a = df_a
        self.df_b = df_b

    def as_dataframe(self):
        df = pd.DataFrame(self.pairs, columns=["src_idx", "trg_idx"])
        R = []
        for idx in list(df["src_idx"]):
            R += [list(self.df_a.iloc[idx])]
        df_a_ = pd.DataFrame(R, columns=["src_"+x for x in list(self.df_a.columns)])
        R = []
        for idx in list(df["trg_idx"]):
            R += [list(self.df_b.iloc[idx])]
        df_b_ = pd.DataFrame(R, columns=["trg_"+x for x in list(self.df_b.columns)])
        return pd.concat([df, df_a_, df_b_], axis=1)
