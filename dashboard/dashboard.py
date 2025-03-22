import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_day_df(df):
    day_df = df.resample(rule='D', on='dteday').agg({
        "instant_y": "nunique",
        "cnt_y": "sum"
    })
    day_df = day_df.reset_index()
    day_df.rename(columns={
        "instant_y": "rent",
        "cnt_y": "total_rent"
    }, inplace=True)
    
    return day_df

def create_weathersit_df(df):
    sum_weathersit_df = df.groupby("weathersit_y").cnt_y.sum().sort_values(ascending=False).reset_index()
    return sum_weathersit_df

def create_season_df(df):
    sum_season_df = df.groupby("season_y").cnt_y.sum().sort_values(ascending=False).reset_index()
    return sum_season_df

def create_weekday_df(df):
    sum_weekday_df = df.groupby("weekday_y").cnt_y.sum().sort_values(ascending=False).reset_index()
    return sum_weekday_df

all_df = pd.read_csv("dashboard/all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

    min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

sum_weathersit_df = create_weathersit_df(main_df)
sum_season_df = create_season_df(main_df)
sum_weekday_df = create_weekday_df(main_df)

weathersit_mapping = {
    1: "Clear",
    2: "Clouds",
    3: "Rain",
    4: "Snowfall"
}

def get_weather_condition(weathersit_num):
    return weathersit_mapping.get(weathersit_num, "Unknown")

sum_weathersit_df['weather_condition'] = sum_weathersit_df['weathersit_y'].apply(get_weather_condition)

print(sum_weathersit_df)

weekday_mapping = {
    5: "Saturday",
    4: "Friday",
    6: "Sunday",
    3: "Thursday",
    2: "Wednesday",
    1: "Tuesday",
    0: "Monday"
}

def get_weekday_condition(weekday_num):
    return weekday_mapping.get(weekday_num, "Unknown")

sum_weekday_df['weekday_condition'] = sum_weekday_df['weekday_y'].apply(get_weekday_condition)

print(sum_weekday_df)

st.header('Dicoding Collection Dashboard :sparkles:')

plt.figure(figsize=(10, 5))

st.subheader("Customer Demographics")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="cnt_y", 
        x="weather_condition",
        data=sum_weathersit_df.sort_values(by="weathersit_y", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Weathersit", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="cnt_y", 
        x="weekday_condition",
        data=sum_weekday_df.sort_values(by="weejday_y", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Weekday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
