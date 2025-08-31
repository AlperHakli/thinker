import dask.dataframe as dd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd




try:
    db = dd.read_csv(r"csv_file_here/Iris.csv")
except FileNotFoundError:
    print("file bulunamadı")

db = db.compute()
column_name = "SepalWidthCm"
column_name2 = "Id"
db = db.select_dtypes(include="number")
ax = sns.heatmap(data=db.corr(),annot=True)
plt.tight_layout()
plt.show()