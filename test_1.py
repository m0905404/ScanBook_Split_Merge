import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplcursors  # pip install mplcursors

# ==== 中文字體設定 ====
plt.rcParams['font.family'] = ['DFKai-SB']  # 你電腦若沒這字體，可改成 Noto Sans CJK TC
plt.rcParams['axes.unicode_minus'] = False

# ==== 原始資料 ====
life_data = {
    "年份": [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,
             2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,
             2021,2022,2023,2024],
    "平均壽命LE": [76.75,77.19,77.35,77.48,77.42,77.90,78.38,78.57,79.01,79.18,
                   79.15,79.51,80.02,79.84,80.20,80.00,80.39,80.69,80.86,81.32,
                   80.86,79.84,80.23,80.77],
    "健康壽命HLE": [69.11,69.21,69.90,69.46,69.54,70.23,70.36,70.49,70.78,71.02,
                   70.83,71.56,71.78,71.58,71.87,71.83,72.07,72.28,72.39,73.28,
                   73.30,72.43,72.45,None],
}

df = pd.DataFrame(life_data)
df["健康壽命HLE"] = df["健康壽命HLE"].interpolate()
df["不健康壽命UHLE"] = df["平均壽命LE"] - df["健康壽命HLE"]

# ==== 外插設定 ====
End_Year = 2035
End_LE = 82
End_Percent = 0.95  # 2035 年健康比例

target_years = np.arange(2025, End_Year + 1)
start_LE = df["平均壽命LE"].iloc[-1]
start_HLE = df["健康壽命HLE"].iloc[-1]
target_LE = np.linspace(start_LE, End_LE, len(target_years))
target_HLE = np.linspace(start_HLE, End_LE * End_Percent, len(target_years))

df_future = pd.DataFrame({
    "年份": target_years,
    "平均壽命LE": target_LE,
    "健康壽命HLE": target_HLE
})
df_future["不健康壽命UHLE"] = df_future["平均壽命LE"] - df_future["健康壽命HLE"]

df_all = pd.concat([df, df_future], ignore_index=True)
df_all["健康比例(%)"] = (df_all["健康壽命HLE"] / df_all["平均壽命LE"]) * 100

# ==== 繪圖 ====
plt.figure(figsize=(12,6))
plt.plot(df_all["年份"], df_all["平均壽命LE"], 'o-', label='平均壽命 LE', color='blue')
plt.plot(df_all["年份"], df_all["健康壽命HLE"], 's-', label='健康壽命 HLE', color='orange')

plt.axvline(x=2024, color='gray', linestyle='--', alpha=0.6)
plt.text(2024.5, df_all["平均壽命LE"].min()+1, "外插區間開始", color='gray', fontsize=10)

plt.xlabel("年份")
plt.ylabel("壽命（年）")
plt.title(f"平均壽命 LE 與健康壽命 HLE（含外插至 {End_Year}）")
plt.legend()
plt.grid(True)

# ==== 滑鼠提示功能 ====
cursor = mplcursors.cursor(hover=True)

@cursor.connect("add")
def on_hover(sel):
    i = sel.index
    year = df_all["年份"].iloc[i]
    le = df_all["平均壽命LE"].iloc[i]
    hle = df_all["健康壽命HLE"].iloc[i]
    ratio = df_all["健康比例(%)"].iloc[i]
    sel.annotation.set_text(
        f"年份：{year}\n"
        f"平均壽命：{le:.2f} 年\n"
        f"健康壽命：{hle:.2f} 年\n"
        f"健康比例：{ratio:.1f}%"
    )
    sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

plt.tight_layout()
plt.show()
