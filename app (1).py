
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px # Import Plotly

st.set_page_config(page_title="Waste Dashboard", layout="wide")

st.title("🌍 Plastic Waste Management Dashboard")

# Load data
df = pd.read_csv("Plastic Waste Around the World.csv")

# Sidebar filter
st.sidebar.header("Filter")
country = st.sidebar.selectbox("Select Country", ["All"] + sorted(df["Country"].unique()))
coastal_risk = st.sidebar.selectbox("Filter by Coastal Waste Risk", ["All", "High", "Medium", "Low"])

# Apply filters
filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]
if coastal_risk != "All":
    filtered_df = filtered_df[filtered_df["Coastal_Waste_Risk"] == coastal_risk]

# Metrics - Use filtered_df
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Countries", len(filtered_df))
col2.metric("Max Waste", f"{filtered_df["Total_Plastic_Waste_MT"].max():.2f}" if not filtered_df.empty else "N/A")
col3.metric("Avg Waste", f"{filtered_df["Total_Plastic_Waste_MT"].mean():.2f}" if not filtered_df.empty else "N/A")

# Graph - Top 10 Countries Bar Chart - Use filtered_df
st.subheader("Top 10 Countries by Plastic Waste")
if not filtered_df.empty:
    top = filtered_df.sort_values(by="Total_Plastic_Waste_MT", ascending=False).head(10)
    fig_bar, ax_bar = plt.subplots()
    sns.barplot(x="Total_Plastic_Waste_MT", y="Country", data=top, ax=ax_bar)
    st.pyplot(fig_bar)
else:
    st.write("No data to display for the selected filters.")


# Graph - Top 5 Countries Contribution - Use filtered_df
st.subheader("Top 5 Countries Contribution")
if not filtered_df.empty:
    top5 = filtered_df.sort_values(by="Total_Plastic_Waste_MT", ascending=False).head(5)
    if not top5.empty:
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(
            top5["Total_Plastic_Waste_MT"],
            labels=top5["Country"],
            autopct='%1.1f%%',
            startangle=90
        )
        ax_pie.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig_pie)
    else:
        st.write("No data to display for the selected filters to generate top 5 contribution.")
else:
    st.write("No data to display for the selected filters.")

# --- New Data Analysis Sections --- (Update all to use filtered_df)

st.subheader("📈 Descriptive Statistics for Numerical Features")
if not filtered_df.empty:
    st.dataframe(filtered_df[['Total_Plastic_Waste_MT', 'Recycling_Rate', 'Per_Capita_Waste_KG']].describe())
else:
    st.write("No data to display for the selected filters.")

st.subheader("Main Sources of Plastic Waste Distribution")
if not filtered_df.empty:
    source_counts = filtered_df["Main_Sources"].value_counts().reset_index()
    source_counts.columns = ["Main_Source", "Count"]

    fig_source, ax_source = plt.subplots()
    sns.barplot(x="Count", y="Main_Source", data=source_counts, ax=ax_source)
    ax_source.set_title("Distribution of Main Plastic Waste Sources")
    ax_source.set_xlabel("Number of Countries")
    ax_source.set_ylabel("Main Source")
    st.pyplot(fig_source)
else:
    st.write("No data to display for the selected filters.")

st.subheader("Average Total Plastic Waste by Main Source")
if not filtered_df.empty:
    avg_waste_by_source = filtered_df.groupby("Main_Sources")["Total_Plastic_Waste_MT"].mean().sort_values(ascending=False).reset_index()

    fig_avg_source, ax_avg_source = plt.subplots()
    sns.barplot(x="Total_Plastic_Waste_MT", y="Main_Sources", data=avg_waste_by_source, ax=ax_avg_source)
    ax_avg_source.set_title("Average Total Plastic Waste by Main Source")
    ax_avg_source.set_xlabel("Average Total Plastic Waste (Million Tonnes)")
    ax_avg_source.set_ylabel("Main Source")
    st.pyplot(fig_avg_source)
else:
    st.write("No data to display for the selected filters.")

st.subheader("Coastal Waste Risk Distribution")
if not filtered_df.empty:
    risk_counts = filtered_df["Coastal_Waste_Risk"].value_counts().reset_index()
    risk_counts.columns = ["Risk_Level", "Count"]

    fig_risk, ax_risk = plt.subplots()
    sns.barplot(x="Count", y="Risk_Level", data=risk_counts, order=["High", "Medium", "Low"], ax=ax_risk)
    ax_risk.set_title("Distribution of Coastal Waste Risk Levels")
    ax_risk.set_xlabel("Number of Countries")
    ax_risk.set_ylabel("Risk Level")
    st.pyplot(fig_risk)
else:
    st.write("No data to display for the selected filters.")

st.subheader("Average Total Plastic Waste by Coastal Waste Risk")
if not filtered_df.empty:
    all_risk_levels = ["High", "Medium", "Low"]
    avg_waste_by_risk = filtered_df.groupby("Coastal_Waste_Risk")["Total_Plastic_Waste_MT"].mean().reindex(all_risk_levels).fillna(0).reset_index()

    fig_avg_risk, ax_avg_risk = plt.subplots()
    sns.barplot(x="Total_Plastic_Waste_MT", y="Coastal_Waste_Risk", data=avg_waste_by_risk, order=all_risk_levels, ax=ax_avg_risk)
    ax_avg_risk.set_title("Average Total Plastic Waste by Coastal Waste Risk")
    ax_avg_risk.set_xlabel("Average Total Plastic Waste (Million Tonnes)")
    ax_avg_risk.set_ylabel("Coastal Waste Risk")
    st.pyplot(fig_avg_risk)
else:
    st.write("No data to display for the selected filters.")

st.subheader("Top 5 Countries by Recycling Rate")
if not filtered_df.empty:
    top_recycling = filtered_df.sort_values(by="Recycling_Rate", ascending=False).head(5)
    fig_recycling, ax_recycling = plt.subplots()
    sns.barplot(x="Recycling_Rate", y="Country", data=top_recycling, ax=ax_recycling)
    ax_recycling.set_title("Top 5 Countries by Recycling Rate")
    ax_recycling.set_xlabel("Recycling Rate (%)")
    ax_recycling.set_ylabel("Country")
    st.pyplot(fig_recycling)
else:
    st.write("No data to display for the selected filters.")

st.subheader("Per Capita Waste vs. Recycling Rate")
if not filtered_df.empty:
    fig_scatter = px.scatter(
        filtered_df,
        x='Per_Capita_Waste_KG',
        y='Recycling_Rate',
        color='Coastal_Waste_Risk',
        hover_name='Country',
        title='Per Capita Waste vs. Recycling Rate by Coastal Waste Risk',
        labels={
            'Per_Capita_Waste_KG': 'Per Capita Waste (KG)',
            'Recycling_Rate': 'Recycling Rate (%)'
        }
    )
    st.plotly_chart(fig_scatter)
else:
    st.write("No data to display for the selected filters.")


st.subheader("Correlation Matrix of Numerical Features")
if not filtered_df.empty:
    numerical_df = filtered_df[['Total_Plastic_Waste_MT', 'Recycling_Rate', 'Per_Capita_Waste_KG']]
    correlation_matrix = numerical_df.corr()

    fig_corr, ax_corr = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=".5", ax=ax_corr)
    ax_corr.set_title('Correlation Matrix of Numerical Features')
    st.pyplot(fig_corr)
else:
    st.write("No data to display for the selected filters.")

# Country details - Show original data for the selected country, or a message if 'All' is selected
st.subheader("🔍 Country Analysis")
if country != "All":
    st.write(df[df["Country"] == country])
else:
    st.write("Select a specific country from the sidebar for detailed analysis.")
