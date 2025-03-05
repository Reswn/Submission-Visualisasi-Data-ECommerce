import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    customers_df = pd.read_csv("customers_dataset.csv")
    order_items_df = pd.read_csv("order_items_dataset.csv")
    return customers_df, order_items_df

customers_df, order_items_df = load_data()

# Sidebar - Pemilihan Dataset
dataset_choice = st.sidebar.selectbox("Pilih Dataset", ["Pelanggan", "Item Pesanan"])

st.title("Dasbor E-commerce: Data Pelanggan dan Item Pesanan")

# Analisis Dataset Pelanggan
if dataset_choice == "Pelanggan":
    st.header("Analisis Pelanggan")

    # Jumlah pelanggan unik
    unique_customers = customers_df["customer_unique_id"].nunique()
    st.metric(label="Total Pelanggan Unik", value=unique_customers)

    # Distribusi pelanggan berdasarkan kota
    city_counts = customers_df["customer_city"].value_counts().head(10)
    fig_city = px.bar(
        x=city_counts.index, 
        y=city_counts.values, 
        labels={"x": "Kota", "y": "Jumlah Pelanggan"},
        title="10 Kota dengan Pelanggan Terbanyak", 
        color=city_counts.index
    )
    st.plotly_chart(fig_city)

    # Distribusi pelanggan berdasarkan provinsi
    state_counts = customers_df["customer_state"].value_counts()
    fig_state = px.pie(
        values=state_counts.values, 
        names=state_counts.index, 
        title="Distribusi Pelanggan berdasarkan Provinsi"
    )
    st.plotly_chart(fig_state)

# Analisis Dataset Item Pesanan
elif dataset_choice == "Item Pesanan":
    st.header("Analisis Item Pesanan")

    # Distribusi harga produk
    fig_price = px.histogram(order_items_df, x="price", nbins=30, title="Distribusi Harga Produk")
    st.plotly_chart(fig_price)

    # Total biaya pengiriman berdasarkan penjual
    seller_freight = (
        order_items_df.groupby("seller_id")["freight_value"]
        .sum()
        .reset_index()
        .sort_values(by="freight_value", ascending=False)
        .head(10)
    )
    fig_freight = px.bar(
        seller_freight, 
        x="seller_id", 
        y="freight_value", 
        title="10 Penjual dengan Biaya Pengiriman Tertinggi", 
        color="seller_id"
    )
    st.plotly_chart(fig_freight)

    # Jumlah item per pesanan
    order_count = order_items_df["order_id"].value_counts().reset_index()
    order_count.columns = ["order_id", "jumlah_item"]
    fig_order_count = px.histogram(
        order_count, 
        x="jumlah_item", 
        nbins=20, 
        title="Distribusi Jumlah Item dalam Pesanan"
    )
    st.plotly_chart(fig_order_count)

st.sidebar.info("Pilih dataset dari sidebar untuk menganalisis pelanggan atau item pesanan.")
