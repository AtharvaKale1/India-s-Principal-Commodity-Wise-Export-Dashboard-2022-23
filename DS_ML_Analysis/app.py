import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned dataset
df = pd.read_excel(r"C:\Users\athar\OneDrive\Desktop\College\DS_ML_Analysis\Cleaned_Principal_Commodity_Exports_with_clusters.xlsx", engine='openpyxl')

# Page configuration
st.set_page_config(page_title="India's Export Analysis Dashboard", layout="wide")
st.title("🇮🇳 India's Principal Commodity-wise Export Dashboard (2022–23)")

# Sidebar Filters
st.sidebar.header("🔎 Filter the Data")
countries = st.sidebar.multiselect("Select Country", df["COUNTRY"].unique(), default=df["COUNTRY"].unique())
commodities = st.sidebar.multiselect("Select Commodity", df["COMMODITY_NAME"].unique(), default=df["COMMODITY_NAME"].unique())
clusters = st.sidebar.multiselect("Select Cluster", df["Cluster"].unique(), default=df["Cluster"].unique())

# Apply filters
filtered_df = df[
    (df["COUNTRY"].isin(countries)) &
    (df["COMMODITY_NAME"].isin(commodities)) &
    (df["Cluster"].isin(clusters))
]

# KPIs
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Export Value (USD Million)", f"{filtered_df['VALUE_USD_MILLION'].sum():,.2f}")
col2.metric("Total Quantity (Kgs)", f"{filtered_df['QUANTITY_KGS'].sum():,.2f}")
col3.metric("Average Price per KG", f"{filtered_df['PRICE_PER_KG'].mean():.2f} USD/kg")
col4.metric("Total Unique Commodities", filtered_df['COMMODITY_NAME'].nunique())

# Expensive Commodities
st.subheader("💰 Top 10 Most Expensive Commodities (per KG)")
top_exp = filtered_df.sort_values("PRICE_PER_KG", ascending=False).drop_duplicates("COMMODITY_NAME")
st.dataframe(top_exp[["COMMODITY_NAME", "PRICE_PER_KG", "COUNTRY"]].head(10), use_container_width=True)

# Cheapest Commodities
st.subheader("🪙 Top 10 Cheapest Commodities (per KG)")
top_cheap = filtered_df.sort_values("PRICE_PER_KG", ascending=True).drop_duplicates("COMMODITY_NAME")
st.dataframe(top_cheap[["COMMODITY_NAME", "PRICE_PER_KG", "COUNTRY"]].head(10), use_container_width=True)

# Top Countries by Export Value
st.subheader("🌍 Top 10 Countries by Export Value")
top_countries = filtered_df.groupby("COUNTRY")["VALUE_USD_MILLION"].sum().nlargest(10).reset_index()
fig1 = px.bar(top_countries, x="VALUE_USD_MILLION", y="COUNTRY", orientation='h', color="VALUE_USD_MILLION",
              color_continuous_scale="blues", labels={'VALUE_USD_MILLION': 'Value (USD Million)'},
              title="Top Export Destinations")
st.plotly_chart(fig1, use_container_width=True)

# Cluster-wise Distribution
st.subheader("🔹 Cluster Distribution (KMeans)")
fig2 = px.pie(filtered_df, names="Cluster", title="Distribution by Cluster", hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

# Data Table
st.subheader("📄 Explore the Data")
st.dataframe(filtered_df, use_container_width=True)