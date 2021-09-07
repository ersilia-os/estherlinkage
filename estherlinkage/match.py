
COLUMNS = [
    "identifier",
    "first_name",
    "last_name",
    "sex",
    "birth_date",
    "visit_date"
]

class Match():

    def __init__(self, mapping):
        self.mapping = mapping

    def match(self, df):
        df = df.rename(columns = self.mapping)
        return df[COLUMNS]
