import pandas as pd
import os
from matplotlib import pyplot as plt
import tqdm

def plot_grid_donut_charts(names, values):
    if len(names) != 16 or len(values) != 16:
        raise ValueError("As listas devem conter exatamente 16 elementos cada.")

    total = 25000
    _, axs = plt.subplots(4, 4, figsize=(12, 12))
    axs = axs.flatten()

    for i in range(16):
        filled = values[i]
        remainder = total - filled
        percent = (filled/total)*100
        # Desenha a rosca
        wedges, texts = axs[i].pie(
            [filled, remainder],
            startangle=90,
            counterclock=False,
            colors=["#4CAF50", "#DDDDDD"],
            wedgeprops=dict(width=0.4)
        )
        axs[i].set_title(names[i], fontsize=10)
        axs[i].axis("equal")  # Rosca circular
        # Adiciona valor no centro
        axs[i].text(0, 0, f"{percent:.2f}%", ha='center', va='center', fontsize=9, weight='bold')

    plt.tight_layout()
    plt.savefig("./roscas.jpg")

def get_class_map():
    return {
        0: "letter",
        1: "form",
        2: "email",
        3: "handwritten",
        4: "advertisement",
        5: "scientific report",
        6: "scientific publication",
        7: "specification",
        8: "file folder",
        9: "news article",
        10: "budget",
        11: "invoice",
        12: "presentation",
        13: "questionnaire",
        14: "resume",
        15: "memo",
    }

class_map = get_class_map()

df = pd.read_csv("./rvl.txt", sep=" ", header=None)
df.columns = ["path", "class"]
df["path"] = df["path"].apply(lambda a: os.path.basename(a).split(".")[0])
df["class"] = df["class"].apply(lambda a: class_map[a])
df = df.set_index("path")

df_out = pd.read_csv("./dia24-7.csv")
df_out[" clustering"] = df_out[" clustering"].apply(lambda a: a.split(".")[0].strip())
df_out

values = class_map.values()
progress = {elem: 0 for elem in values}

doc_list = df_out[" clustering"].values
for elem in tqdm.tqdm(doc_list):
    try:
        v = df.loc[elem].iloc[0]
        progress[v] += 1
    except:
        pass

plot_grid_donut_charts(list(progress.keys()), list(progress.values()))