import pandas as pd

MILLENIUM_CUT = 25

class Clean(object):

    def __init__(self):
        pass

    def string(self, series):
        vals = []
        for s in list(series):
            s = str(s)
            if s == "nan":
                vals += [None]
            else:
                vals += [s.lower()]
        return vals

    def date(self, series):
        vals = []
        for date in list(series):
            date = str(date)
            if date[-3] == "/":
                d, m, y = date.split("/")
                y = int(y)
                if y < MILLENIUM_CUT:
                    y = "20%02d" % y
                else:
                    y = "19%02d" % y
                date = "%s-%s-%s" % (y, m, d)
            vals += [date]
        return pd.to_datetime(vals)
