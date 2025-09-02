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
column_name = "Species"
column_name2 = "SepalLengthCm"

ax = sns.violinplot(data=db , x=column_name , y = column_name2  , color= "blue" , linecolor="red" )
ax.set_facecolor("grey")

ax.tick_params(axis="x" , labelcolor = "purple")
ax.set_xlabel(xlabel=ax.get_xlabel() , color = "orange")


plt.tight_layout()
plt.show()