import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    return pd.read_csv("all_data.csv")

merged_df = load_data()

st.title("📊 Dashboard Peminjaman Sepeda")
st.write("Visualisasi data peminjaman sepeda berdasarkan musim, waktu, dan hari.")

graph_choice = st.selectbox("Pilih visualisasi yang ingin ditampilkan:", 
                           ["Bagaimana performa peminjaman sepeda pada setiap musim di tahun 2011 dan 2012?", 
                            "Bagaimana pola peminjaman sepeda pada pagi, siang, sore, dan malam?", 
                            "Pada hari apa peminjaman sepeda paling sedikit?"])

if graph_choice == "Bagaimana performa peminjaman sepeda pada setiap musim di tahun 2011 dan 2012?":
    season_summary = merged_df.groupby(["yr", "season"])[["casual", "registered", "cnt"]].sum().reset_index()
    season_mapping = {1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"}
    season_summary["season"] = season_summary["season"].map(season_mapping)

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(8, 5))

    ax = sns.barplot(data=season_summary, x="season", y="cnt", hue="yr", palette="rocket")

    plt.xlabel("Musim", fontsize=12)
    plt.ylabel("Total Peminjaman Sepeda", fontsize=12)
    plt.title("Performa Peminjaman Sepeda di Setiap Musim (2011 vs 2012)", fontsize=14)

    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles=handles, labels=["2011", "2012"], title="Tahun") 
    st.pyplot(fig)

elif graph_choice == "Bagaimana pola peminjaman sepeda pada pagi, siang, sore, dan malam?":
    time_summary = merged_df.groupby("hour_group")["cnt"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=time_summary, x="hour_group", y="cnt", color="royalblue", ax=ax)
    ax.set_xlabel("Waktu dalam Sehari")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_title("Pola Peminjaman Berdasarkan Waktu")
    st.pyplot(fig)

elif graph_choice == "Pada hari apa peminjaman sepeda paling sedikit?":
    weekday_summary = merged_df.groupby("weekday")[["cnt"]].sum().reset_index()
    sns.set_style("ticks")
    day_labels = {
        0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis",
        4: "Jumat", 5: "Sabtu", 6: "Minggu"
    }

    weekday_summary["weekday"] = weekday_summary["weekday"].map(day_labels)
    weekday_summary_sorted = weekday_summary.sort_values("cnt")
    base_color = "#D3D3D3"  
    highlight_color = "#72BCD4"  
    colors = [highlight_color if i == weekday_summary_sorted["cnt"].min() else base_color for i in weekday_summary_sorted["cnt"]]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weekday_summary_sorted, y="weekday", x="cnt", hue="weekday", palette=colors, ax=ax)

    ax.set_xlabel("Total Peminjaman Sepeda", fontsize=12)
    ax.set_ylabel("Hari", fontsize=12)
    ax.set_title("Peminjaman Sepeda Berdasarkan Hari", fontsize=14)
    ax.tick_params(axis="x", labelsize=10)
    st.pyplot(fig)
