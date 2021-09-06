import pandas as pd

# Read data
df_src = pd.read_csv("/Users/mduran/Desktop/module2_example/source.csv")
df_trg = pd.read_csv("/Users/mduran/Desktop/module2_example/target.csv")
df_gld = pd.read_csv("/Users/mduran/Desktop/module2_example/truth.csv")

print(df_src)
print(df_trg)
print(df_gld)

# Some preprocessing
df_src["Birth_Date"] = pd.to_datetime(df_src["Birth_Date"])
df_trg[""]

# Block
from estherlinkage import Block
bl = Block(df_trg, columns=["first_name", "last_name"], k=5)
pairs = bl.block(df_src, columns=["Given Name", "Family Name"])
print(pairs)

# Compare
from estherlinkage import Compare
comp = Compare()
comp.exact("Unique Id", "identifier")
comp.string("Given Name", "first_name", method="jarowinkler")
comp.string("Given Name", "first_name", method="levenshtein")
comp.string("Family Name", "last_name", method="jarowinkler")
comp.string("Family Name", "last_name", method="levenshtein")
comp.exact("Gender", "sex")
comp.date("Birth_Date", "birth_date")
comp.date("Date Of Visit", "visit_date")
features = comp.compute(pairs, df_src, df_trg)
print(features)

# Splits
from estherlinkage import Split
spl = Split(test_size=0.2)
splits = spl.split()
