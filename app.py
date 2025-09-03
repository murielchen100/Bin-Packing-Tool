import streamlit as st
import pandas as pd
import itertools

st.title("鑽石分包最佳化工具")

diamond_file = st.file_uploader("上傳鑽石重量 Excel", type=["xlsx"])
package_file = st.file_uploader("上傳分包規定 Excel", type=["xlsx"])

tolerance = st.number_input("容許誤差 (ct)", value=0.003, step=0.001)

if diamond_file and package_file:
    diamonds_df = pd.read_excel(diamond_file)
    packages_df = pd.read_excel(package_file)

    diamonds = diamonds_df.iloc[:, 0].tolist()
    results = []
    used_indices = set()

    for idx, row in packages_df.iterrows():
        count = int(row[0])
        target = float(row[1])
        found = False

        available = [i for i in range(len(diamonds)) if i not in used_indices]
        for combo_indices in itertools.combinations(available, count):
            combo = [diamonds[i] for i in combo_indices]
            if abs(sum(combo) - target) <= tolerance:
                results.append({
                    "分包編號": idx+1,
                    "分配鑽石": combo,
                    "總重": sum(combo)
                })
                used_indices.update(combo_indices)
                found = True
                break

        if not found:
            results.append({
                "分包編號": idx+1,
                "分配鑽石": "找不到符合組合",
                "總重": "-"
            })

    st.write("分配結果：")
    for res in results:

        st.write(f"分包{res['分包編號']}：{res['分配鑽石']}，總重：{res['總重']}")
