import dask.dataframe as dd
import seaborn as sns
import matplotlib.pyplot as plt





try:
    db = dd.read_csv(r"C:\Users\Alper\PycharmProjects\thinker\csv_file_here\Iris.csv")
except FileNotFoundError:
    print("file bulunamadı")

db = db.select_dtypes(include=["number"])



sns.set_style("white" ,{
    "axes.facecolor" : "green",
    "figure.facecolor" : "black",
    "bar.facecolor" : "black",
    "grid.color" : "yellow"
})

ax = sns.barplot(x = db["SepalLengthCm"] ,y = db["Id"])
fig = plt.gcf()
axes = plt.gca()
sns.set_theme(style="dark")
fig.canvas.manager.set_window_title("BarPlot")
plt.tick_params(axis="x" , colors = "white")
plt.tick_params(axis="y" , colors = "green")
ax.set_xlabel(ax.get_xlabel() , color = "yellow")
plt.xticks(rotation = 90)
plt.show()


# Index(['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm'], dtype='object')