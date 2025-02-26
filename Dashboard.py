import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    return pd.read_csv("all_data.csv")

merged_df = load_data()

merged_df["dteday"] = pd.to_datetime(merged_df["dteday"])

st.sidebar.header("📅 Filter Rentang Tanggal")
min_date = merged_df["dteday"].min()
max_date = merged_df["dteday"].max()

start_date = st.sidebar.date_input("Mulai dari:", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Sampai dengan:", max_date, min_value=min_date, max_value=max_date)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

if start_date > end_date:
    st.sidebar.error("⚠️ Tanggal mulai harus lebih kecil atau sama dengan tanggal akhir.")
else:
    # Filter dataset berdasarkan rentang tanggal
    filtered_df = merged_df[(merged_df["dteday"] >= start_date) & (merged_df["dteday"] <= end_date)]

    # Total jumlah peminjaman sepeda
    total_pinjaman = filtered_df["cnt"].sum()

    # Plot jumlah peminjaman sepeda per hari
    st.subheader(f"Tren Peminjaman Sepeda per Hari (Total: {total_pinjaman})")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=filtered_df["dteday"], y=filtered_df["cnt"], marker='o', color='b', ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Peminjaman Sepeda")
    ax.set_title("Tren Peminjaman Sepeda per Hari")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

    # Dashboard
    st.title("📊 Dashboard Peminjaman Sepeda")
    st.write("Visualisasi data peminjaman sepeda berdasarkan musim, waktu, dan hari.")

    graph_choice = st.selectbox("Pilih visualisasi yang ingin ditampilkan:", 
                               ["Bagaimana performa peminjaman sepeda pada setiap musim di tahun 2011 dan 2012?", 
                                "Bagaimana pola peminjaman sepeda pada pagi, siang, sore, dan malam?", 
                                "Pada hari apa peminjaman sepeda paling sedikit?"])

    if graph_choice == "Bagaimana performa peminjaman sepeda pada setiap musim di tahun 2011 dan 2012?":
        season_summary = filtered_df.groupby(["yr", "season"])[["casual", "registered", "cnt"]].sum().reset_index()
        season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
        season_summary["season"] = season_summary["season"].map(season_mapping)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=season_summary, x="season", y="cnt", hue="yr", palette="rocket", ax=ax)
        ax.set_xlabel("Musim", fontsize=12)
        ax.set_ylabel("Total Peminjaman Sepeda", fontsize=12)
        ax.set_title("Performa Peminjaman Sepeda di Setiap Musim (2011 vs 2012)", fontsize=14)
        handles, labels = ax.get_legend_handles_labels()
        plt.legend(handles=handles, labels=["2011", "2012"], title="Tahun") 
        st.pyplot(fig)

    elif graph_choice == "Bagaimana pola peminjaman sepeda pada pagi, siang, sore, dan malam?":
        time_summary = filtered_df.groupby("hour_group")["cnt"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=time_summary, x="hour_group", y="cnt", color="royalblue", ax=ax)
        ax.set_xlabel("Waktu dalam Sehari")
        ax.set_ylabel("Jumlah Peminjaman")
        ax.set_title("Pola Peminjaman Berdasarkan Waktu")
        st.pyplot(fig)

    elif graph_choice == "Pada hari apa peminjaman sepeda paling sedikit?":
        weekday_summary = filtered_df.groupby("weekday")[["cnt"]].sum().reset_index()
        day_labels = {
            0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis",
            4: "Jumat", 5: "Sabtu", 6: "Minggu"
        }
        weekday_summary["weekday"] = weekday_summary["weekday"].map(day_labels)
        weekday_summary_sorted = weekday_summary.sort_values("cnt")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=weekday_summary_sorted, y="weekday", x="cnt", palette="coolwarm", ax=ax)
        ax.set_xlabel("Total Peminjaman Sepeda", fontsize=12)
        ax.set_ylabel("Hari", fontsize=12)
        ax.set_title("Peminjaman Sepeda Berdasarkan Hari", fontsize=14)
        st.pyplot(fig)
