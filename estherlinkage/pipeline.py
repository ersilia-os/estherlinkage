from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import precision_score, recall_score, f1_score

from . import Match
from . import Clean
from . import Block
from . import Compare
from . import Split
from . import Assemble

# Match step

def match(df, cols):
    return Match(cols).match(df)

# Preprocess step

def preprocess(df):
    cl = Clean()
    for col in list(df.columns):
        if col in ["birth_date", "visit_date"]:
            df[col] = cl.date(df[col])
        else:
            df[col] = cl.string(df[col])
    return df

# Blocking step

def block(df_a, df_b, columns=["first_name", "last_name"], k=5):
    bl = Block(df_b, columns, k)
    return bl.block(df_a, columns)

# Comparisons step

def compare(pairs, df_a, df_b, df_g):
    comp = Compare()
    comp.exact("identifier", "identifier", label="id")
    comp.string("first_name", "first_name", method="jarowinkler", label="fn_jw")
    comp.string("first_name", "first_name", method="levenshtein", label="fn_lv")
    comp.string("last_name", "last_name", method="jarowinkler", label="ln_jw")
    comp.string("last_name", "last_name", method="levenshtein", label="ln_lv")
    comp.exact("sex", "sex", label="sex")
    comp.date("birth_date", "birth_date", label="bdate")
    comp.date("visit_date", "visit_date", label="vdate")
    features = comp.compute(pairs, df_a, df_b)
    spl = Split(train_size=0.5)
    splits = spl.split(features, df_g)
    return splits

# Scoring

def score_and_validate(splits):
    clf = LogisticRegressionCV()
    pairs = splits["pairs"]
    X = splits["X"]
    y = splits["y"]
    train_idx = splits["train_idx"]
    valid_idx = splits["valid_idx"]
    X_train = X[train_idx]
    y_train = y[train_idx]
    X_valid = X[valid_idx]
    y_valid = y[valid_idx]
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_valid)
    print("Precision", precision_score(y_valid, y_pred))
    print("Recall", recall_score(y_valid, y_pred))
    print("F1-score", f1_score(y_valid, y_pred))
    return clf.predict(X)

# Assemble results

def assemble(pairs, y, df_a, df_b):
    a = Assemble(pairs, y, df_a, df_b)
    return a.as_dataframe()

# End to end pipeline

def end2end_pipeline(df_src, df_trg, df_gld, cols_src):
    df_src = match(df_src, cols_src)
    df_src = preprocess(df_src)
    df_trg = preprocess(df_trg)
    pairs = block(df_src, df_trg)
    splits = compare(pairs, df_src, df_trg, df_gld)
    y_pred = score_and_validate(splits)
    df_res = assemble(splits["pairs"], y_pred, df_src, df_trg)
    return df_res
