import pandas as pd

# Read data
df_src = pd.read_csv("/Users/mduran/Desktop/module2_example/source.csv")
df_trg = pd.read_csv("/Users/mduran/Desktop/module2_example/target.csv")
df_gld = pd.read_csv("/Users/mduran/Desktop/module2_example/truth.csv")

# Some preprocessing
from estherlinkage import Clean
cl = Clean()
df_src["Birth_Date"] = cl.date(df_src["Birth_Date"])
df_src["Birth_Date"] = cl.date(df_src["Birth_Date"])
df_src["Date Of Visit"] = cl.date(df_src["Date Of Visit"])
df_trg["birth_date"] = cl.date(df_trg["birth_date"])
df_trg["visit_date"] = cl.date(df_trg["visit_date"])

# Block
from estherlinkage import Block
bl = Block(df_trg, columns=["first_name", "last_name"], k=5)
pairs = bl.block(df_src, columns=["Given Name", "Family Name"])

# Compare
from estherlinkage import Compare
comp = Compare()
comp.exact("Unique Id", "identifier", label="id")
comp.string("Given Name", "first_name", method="jarowinkler", label="fn_jw")
comp.string("Given Name", "first_name", method="levenshtein", label="fn_lv")
comp.string("Family Name", "last_name", method="jarowinkler", label="ln_jw")
comp.string("Family Name", "last_name", method="levenshtein", label="ln_lv")
comp.exact("Gender", "sex", label="sex")
comp.date("Birth_Date", "birth_date", label="bdate")
comp.date("Date Of Visit", "visit_date", label="vdate")
features = comp.compute(pairs, df_src, df_trg)

# Splits
from estherlinkage import Split
spl = Split(train_size=0.5)
splits = spl.split(features, df_gld)

# Train model
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
X = splits["X"]
y = splits["y"]
train_idx = splits["train_idx"]
valid_idx = splits["valid_idx"]
X_train = X[train_idx]
y_train = y[train_idx]
X_valid = X[valid_idx]
y_valid = y[valid_idx]

clf.fit(X_train, y_train)

# Predict
y_pred = clf.predict(X_valid)

# Scoring
from sklearn.metrics import precision_score, recall_score, f1_score
