import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Job Market Insights", page_icon="📊", layout="wide")

# Load dataset (Reduce memory usage by sampling data)
df = pd.read_csv("D:\IIT Gandhinagar\Off-Campus\Projects\Job Insights Web App\data\job_postings.csv")
df = df.sample(n=50000, random_state=42)  # Load a smaller subset to avoid memory issues

# Convert 'Salary Range' to numeric by extracting numbers
df["Salary Range"] = df["Salary Range"].astype(str).str.replace(r"[^\d\-]", "", regex=True)  # Remove non-numeric characters
df["Salary Range"] = df["Salary Range"].str.split("-").str[0]  # Take the lower bound if it's a range
df["Salary Range"] = pd.to_numeric(df["Salary Range"], errors="coerce")  # Convert to numeric
df = df.dropna(subset=["Salary Range"])  # Remove rows where conversion failed

# Sidebar Styling
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=100)
st.sidebar.title("🔍 Job Filters")
work_type = st.sidebar.multiselect("💼 Select Work Type:", df["Work Type"].unique())
min_salary, max_salary = st.sidebar.slider("💰 Salary Range (in 1000s):", int(df["Salary Range"].min(skipna=True)), int(df["Salary Range"].max(skipna=True)), (50, 70))

# Apply filters
filtered_df = df.copy()
if work_type:
    filtered_df = filtered_df[filtered_df["Work Type"].isin(work_type)]
filtered_df = filtered_df[(filtered_df["Salary Range"] >= min_salary) & (filtered_df["Salary Range"] <= max_salary)]

# Main dashboard
st.markdown("<h1 style='text-align: center; color: #3366ff;'>📊 Job Market Insights Dashboard</h1>", unsafe_allow_html=True)

# Salary Distribution
st.subheader("💰 Salary Distribution")
fig_salary = px.histogram(filtered_df, x="Salary Range", nbins=50, title="Salary Distribution", color_discrete_sequence=["#1f77b4"])
st.plotly_chart(fig_salary, use_container_width=True)

# Job Demand by Country
st.subheader("🌍 Job Demand by Country")
df_country = df["Country"].value_counts().reset_index()
df_country.columns = ["Country", "count"]
fig_demand = px.bar(df_country, x="Country", y="count", title="Job Demand by Country", color_discrete_sequence=["#ff7f0e"])
st.plotly_chart(fig_demand, use_container_width=True)

# Experience Level Analysis
st.subheader("📈 Experience Level Distribution")
fig_exp = px.pie(filtered_df, names="Experience", title="Experience Level Distribution", color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig_exp)

# Job Role Distribution
st.subheader("🛠 Job Role Distribution")
df_roles = df["Role"].value_counts().reset_index()
df_roles.columns = ["Role", "count"]
fig_roles = px.bar(df_roles, x="Role", y="count", title="Job Role Distribution", color_discrete_sequence=["#2ca02c"])
st.plotly_chart(fig_roles, use_container_width=True)

# Display filtered data table
st.subheader("📋 Filtered Job Listings")
# Limit displayed rows to prevent crashes
MAX_ROWS = 500  # Show only the first 500 rows

if len(filtered_df) > MAX_ROWS:
    st.warning(f"Showing only the first {MAX_ROWS} rows out of {len(filtered_df)} available.")
    st.dataframe(filtered_df.head(MAX_ROWS))  # Show a subset without styling
else:
    st.dataframe(filtered_df.style.set_properties(**{'background-color': '#f9f9f9', 'color': '#333', 'border-color': 'black'}))

