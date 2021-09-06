from recordlinkage import Compare as BaseCompare


class Compare(BaseCompare):

    def __init__(self):
        BaseCompare.__init__(self)

    def compute(self, pairs, df_s, df_t):
        features = super().compute(pairs, df_s, df_t)
        return features
