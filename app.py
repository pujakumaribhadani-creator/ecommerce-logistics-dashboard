import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="E-commerce Logistics Dashboard",
    page_icon="📦",
    layout="wide"
)

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("📦 E-commerce Logistics Dashboard")
st.markdown("### Logistics Performance & Customer Insights")
st.markdown("---")
# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("ecommerce_logistics.csv")
# -----------------------------
# Sidebar Information
# -----------------------------

st.sidebar.title("📦 Logistics Dashboard")

st.sidebar.markdown("### Created By")
st.sidebar.success("Puja Kumari")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🛠️ Tools Used")
st.sidebar.write("• Python")
st.sidebar.write("• Pandas")
st.sidebar.write("• Plotly")
st.sidebar.write("• Streamlit")

st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Dataset")
st.sidebar.info("25,000 Orders")

st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Project")
st.sidebar.write("✔ Sales Analysis")
st.sidebar.write("✔ Logistics Analysis")
st.sidebar.write("✔ Customer Experience")
st.sidebar.write("✔ Fraud Detection")
st.markdown("## 🔍 Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    category = st.selectbox(
        "📦 Product Category",
        ["All"] + list(df["product_category"].unique())
    )

with col2:
    shipping = st.selectbox(
        "🚚 Shipping Method",
        ["All"] + list(df["shipping_method"].unique())
    )

with col3:
    warehouse = st.selectbox(
        "🏭 Warehouse",
        ["All"] + list(df["warehouse_location"].unique())
    )

with col4:
    segment = st.selectbox(
        "👥 Customer Segment",
        ["All"] + list(df["customer_segment"].unique())
    )

filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[filtered_df["product_category"] == category]

if shipping != "All":
    filtered_df = filtered_df[filtered_df["shipping_method"] == shipping]

if warehouse != "All":
    filtered_df = filtered_df[filtered_df["warehouse_location"] == warehouse]

if segment != "All":
    filtered_df = filtered_df[filtered_df["customer_segment"] == segment]
    

# -----------------------------
# KPI Calculation
# -----------------------------

total_orders = filtered_df["order_id"].nunique()

total_revenue = filtered_df["total_order_value_usd"].sum()

avg_order_value = filtered_df["total_order_value_usd"].mean()

avg_delay = filtered_df["delivery_delay_days"].mean()

avg_rating = filtered_df["customer_review_score"].mean()

return_rate = (
    (filtered_df["product_returned"] == "Yes").mean() * 100
)

fraud_rate = (
    (filtered_df["fraud_flag"] == "Yes").mean() * 100
)

on_time = (
    (filtered_df["delivery_status"] == "On Time").mean() * 100
)
# ==============================
# KPI Cards
# ==============================

st.markdown("## 📊 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("📦 Total Orders", f"{total_orders:,}")

with kpi2:
    st.metric("💰 Total Revenue", f"${total_revenue/1000000:.2f}M")

with kpi3:
    st.metric("💵 Avg Order Value", f"${avg_order_value:.2f}")

with kpi4:
    st.metric("🚚 On-Time Delivery", f"{on_time:.1f}%")

kpi5, kpi6, kpi7, kpi8 = st.columns(4)

with kpi5:
    st.metric("⭐ Avg Rating", f"{avg_rating:.2f}")

with kpi6:
    st.metric("🔄 Return Rate", f"{return_rate:.1f}%")

with kpi7:
    st.metric("🚨 Fraud Rate", f"{fraud_rate:.1f}%")

with kpi8:
    st.metric("⏳ Avg Delay", f"{avg_delay:.2f} Days")


# ==============================
# Sales & Delivery Analysis
# ==============================

st.markdown("---")
st.subheader("📈 Sales & Delivery Analysis")

chart1, chart2 = st.columns(2)

# Revenue by Category
with chart1:

    revenue = (
        filtered_df.groupby("product_category")["total_order_value_usd"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        revenue,
        x="product_category",
        y="total_order_value_usd",
        color="product_category",
        text_auto=".2s",
        title="Revenue by Product Category",
        height=380
    )

    fig1.update_layout(
        title_x=0.25,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig1, use_container_width=True)

# Delivery Status
with chart2:

    status = (
        filtered_df["delivery_status"]
        .value_counts()
        .reset_index()
    )

    status.columns = ["Delivery Status", "Count"]

    fig2 = px.pie(
        status,
        names="Delivery Status",
        values="Count",
        hole=0.60,
        title="Delivery Status Distribution",
        height=380
    )

    fig2.update_layout(
        title_x=0.22,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("---")
# ==============================
# Logistics Performance
# ==============================

# ==============================
# Logistics Performance
# ==============================

st.markdown("---")
st.subheader("🚚 Logistics Performance")

col1, col2 = st.columns(2)

# Average Delivery Delay by Shipping Method
with col1:

    shipping_delay = (
        filtered_df.groupby("shipping_method")["delivery_delay_days"]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        shipping_delay,
        x="shipping_method",
        y="delivery_delay_days",
        color="shipping_method",
        text_auto=".2f",
        title="Average Delivery Delay by Shipping Method",
        height=380
    )

    fig3.update_layout(
        title_x=0.20,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig3, use_container_width=True)


# Weather Impact on Delivery Delay
with col2:

    weather = (
        filtered_df.groupby("weather_conditions_at_dispatch")["delivery_delay_days"]
        .mean()
        .reset_index()
    )

    fig4 = px.bar(
        weather,
        x="weather_conditions_at_dispatch",
        y="delivery_delay_days",
        color="weather_conditions_at_dispatch",
        text_auto=".2f",
        title="Weather Impact on Delivery Delay",
        height=380
    )

    fig4.update_layout(
        title_x=0.20,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig4, use_container_width=True)
    # ==============================
# Warehouse & Returns Analysis
# ==============================

st.markdown("---")
st.subheader("🏭 Warehouse & Returns Analysis")

col1, col2 = st.columns(2)

# Warehouse Performance
with col1:

    warehouse_perf = (
        filtered_df.groupby("warehouse_location")["delivery_delay_days"]
        .mean()
        .reset_index()
    )

    fig5 = px.bar(
        warehouse_perf,
        x="warehouse_location",
        y="delivery_delay_days",
        color="warehouse_location",
        text_auto=".2f",
        title="Average Delivery Delay by Warehouse",
        height=380
    )

    fig5.update_layout(
        title_x=0.18,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig5, use_container_width=True)

# Product Returns
with col2:

    returns = (
        filtered_df[filtered_df["product_returned"] == "Yes"]
        .groupby("product_category")
        .size()
        .reset_index(name="Returned Orders")
    )

    fig6 = px.bar(
        returns,
        x="product_category",
        y="Returned Orders",
        color="product_category",
        text_auto=True,
        title="Returned Orders by Product Category",
        height=380
    )

    fig6.update_layout(
        title_x=0.18,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("---")
# ==============================
# Fraud & Customer Review
# ==============================

st.markdown("---")
st.subheader("🚨 Fraud & Customer Review")

col1, col2 = st.columns(2)

# Fraud Analysis
with col1:

    fraud = (
        filtered_df.groupby("payment_method")["fraud_flag"]
        .apply(lambda x: (x == "Yes").sum())
        .reset_index(name="Fraud Cases")
    )

    fig7 = px.bar(
        fraud,
        x="payment_method",
        y="Fraud Cases",
        color="payment_method",
        title="Fraud Cases by Payment Method",
        text_auto=True,
        height=380
    )

    fig7.update_layout(
        title_x=0.20,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig7, use_container_width=True)


# Customer Review Distribution
with col2:

    fig8 = px.histogram(
        filtered_df,
        x="customer_review_score",
        color="customer_review_score",
        nbins=5,
        title="Customer Review Score Distribution",
        height=380
    )

    fig8.update_layout(
        title_x=0.20,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig8, use_container_width=True)
    csv = filtered_df.to_csv(index=False)

    st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_logistics_data.csv",
    mime="text/csv"
)
    st.markdown("---")
st.caption(
    "Developed by Puja Kumari | Python • Pandas • Plotly • Streamlit"
)





