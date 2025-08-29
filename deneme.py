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

column_name = "SepalLengthCm"
column_name2 = "SepalWidthCm"
ax = sns.lineplot(x = db[column_name] , y = db[column_name2])
ax.set_facecolor("black")
fig = ax.get_figure()
fig.set_facecolor("blue")


plt.show()