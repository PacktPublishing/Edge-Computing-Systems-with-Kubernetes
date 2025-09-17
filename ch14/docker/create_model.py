import pandas as pd
from sklearn import tree
from joblib import dump

df = pd.read_csv("safety_rules.csv", sep=",", header="infer", encoding="latin-1")
df = df.drop(columns=["object"], errors="ignore")

X = df[["n"]]
y = df["warning_level"]

clf = tree.DecisionTreeRegressor()
clf.fit(X, y)

dump(clf, "safety_rules.model")
