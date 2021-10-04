import os

import pandas as pd


df = pd.read_csv("list.csv", header=0, sep=";", encoding="utf-8")
print(df)


class EnvTemplate:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self._text = f.read()

    def parse(self, data_dict):
        self._res = self._text
        for k, v in data_dict.items():
            self._res = self._res.replace(f"%{k}%", str(v))
        return self._res

    def save_parsed(self, path):
        with open(path, "w+", encoding="utf-8") as f:
            f.write(self._res)


types = {}
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
types_assoc = {"article": 3, "poster": 0, "conference": 1, "these": 7, "autre": 0}

for i in df.index:
    df_ = df.loc[i, :]
    if df_["type"] not in types:
        types[df_["type"]] = 0
    types[df_["type"]] += 1
    dirname = f'{df_["type"]}-{types[df_["type"]]}'
    if not os.path.isdir(dirname):
        print("Creates", dirname)
        os.mkdir(dirname)
    template = EnvTemplate("template.txt")
    if isinstance(df_["date"], float):
        df_["date"] = "en cours"
        df_["publi"] = "en cours"
    if not isinstance(df_["auteur"], float):
        df_["auteur"] = "\n- " + df_["auteur"].replace(", ", "\n- ")
    else:
        df_["auteur"] = ""
    template.parse(
        {
            "title": df_["title"],
            "abstract": "",
            "dirname": dirname,
            "date": df_["date"],
            "auteur": df_["auteur"],
            "publi": df_["publi"],
            "type": types_assoc[str(df_["type"])],
        }
    )
    template.save_parsed(os.path.join(dirname, "index.md"))
