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
column_name = "PetalLengthCm"
column_name2 = "SepalLengthCm"

ax = sns.boxplot(data=db , x=column_name , y = column_name2 , color="red" , linecolor="yellow" ,native_scale=True,legend="full")
ax.set_facecolor("black")

ax.tick_params(axis="x" , labelcolor = "purple")
ax.set_xlabel(xlabel=ax.get_xlabel() , color = "orange")


plt.tight_layout()
plt.show()