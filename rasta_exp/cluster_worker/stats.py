import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import sys


def extract(data, key_list):
    d = {}
    for e in key_list:
        d[e] = data[e]
    return d


tabulate_tools = [["Tool", "Total", "Timeout", "Crash", "Time (s)", "Memory (MB)"]]

if len(sys.argv) < 2:
    print("python3 stats.py directory")
    quit()

print("Going into " + sys.argv[1])
os.chdir(sys.argv[1])

for dir in os.listdir():
    if os.path.isdir(dir):
        print("Processing " + str(dir))
        df = pd.DataFrame()
        # df.astype({"apk_size": int,  "crashed": bool})

        for file in os.listdir(dir):
            with open(dir + "/" + file, "r") as f:
                data = json.load(f)

                d = {}
                d = extract(
                    data, ["crashed", "timeout", "user-cpu-time", "max-rss-mem"]
                )
                d.update(
                    extract(
                        data["apk"], ["apk_size", "min_sdk", "target_sdk", "max_sdk"]
                    )
                )
                df_apk = pd.DataFrame(d, index=[data["apk"]["sha256"]])
                if not df.empty:
                    df = pd.concat([df, df_apk])
                else:
                    df = df_apk

        # print(df)
        # print("Total: " + str(len(df)))
        # print("Crash: " + str(df["crashed"].sum()))
        # print("Average size: " + str(df["apk_size"].mean() / 1000 ** 2) + " Mo ")
        # print("Average size crashed: " + str(df[df["crashed"] == True]["apk_size"].mean() / 1000 ** 2) + " Mo ")
        # print("Average size not crashed: " + str(df[df["crashed"] == False]["apk_size"].mean() / 1000 ** 2) + " Mo ")

        # df.target_sdk.fillna(value='0', inplace=True) # Replace None values by 0
        # #df.replace(to_replace=[None], value=np.nan, inplace=True)
        # df['target_sdk']=df['target_sdk'].astype(int)
        # df.sort_values("target_sdk") # Sort on a column
        #
        # ax = plt.gca()
        # df.plot(kind='scatter',x='target_sdk',y='apk_size', ax=ax)
        # plt.show()

        df["user-cpu-time"] = df["user-cpu-time"].astype(float)  # HACK
        df["max-rss-mem"] = df["max-rss-mem"].astype(float)  # HACK
        cpu = round(df["user-cpu-time"].mean(), 1)
        memory = int(df["max-rss-mem"].mean() / (1000**2))
        tabulate_tools.append(
            [dir, len(df), df["timeout"].sum(), df["crashed"].sum(), cpu, memory]
        )

print(tabulate(tabulate_tools))
print(tabulate(tabulate_tools, tablefmt="latex"))
