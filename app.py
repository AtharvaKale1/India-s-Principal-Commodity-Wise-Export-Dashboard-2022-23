from zipfile import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="India's Export Intelligence Hub",
    page_icon="✨",
    layout="wide",
)

# --- CUSTOM STYLING (CSS) ---
st.markdown("""
<style>
/* Import Font Awesome for icons */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

/* --- TOP HEADER BAR STYLES --- */
.top-bar {
    background-color: #0d1b2a;
    padding: 10px 20px;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.top-bar a {
    color: white;
    text-decoration: none;
    margin-left: 15px;
    font-size: 20px; /* Icon size */
    transition: color 0.3s;
}
.top-bar a:hover {
    color: #007BFF; /* Highlight color on hover */
}
/* -------------------------------------- */

/* Main app background */
.main {
    background-color: #F0F2F6;
}

/* Card-like containers for charts */
div.st-emotion-cache-1r6slb0.e1f1d6gn2 {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Improved Metric Styles */
div[data-testid="stMetric"] {
    background: linear-gradient(to right, #001524, #15616d);
    color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    border: none;
}
div[data-testid="stMetricLabel"] {
    color: rgba(255, 255, 255, 0.7);
}

/* Selectbox styling in the main panel */
div[data-testid="stSelectbox"] > div {
    background-color: #FFFFFF;
    border-radius: 8px;
}

/* --- FULL SIDEBAR & WIDGET STYLES --- */
/* Main sidebar container */
div[data-testid="stSidebar"] {
    background-color: #0d1b2a !important;
}

/* Text elements in sidebar */
div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] label {
    color: white !important;
}

/* Multiselect widget container */
div[data-testid="stMultiSelect"] {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
}
/* Text inside multiselect box */
.st-emotion-cache-1q8d0a5, .st-emotion-cache-4oy321 {
    color: white;
}
/* Selected item "pills" */
.st-emotion-cache-1q8d0a5 > div {
    background-color: #007BFF;
}

/* ### --- SLIDER STYLE CHANGES --- ### */
/* Inactive slider track */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child {
    background-color: #44475a; /* Darker, professional track */
}
/* Active slider track */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div:nth-child(2) {
    background-color: #8A2BE2; /* Vibrant purple */
}
/* Slider handle */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div:nth-child(3) {
    border: 3px solid #8A2BE2; /* Matching purple border */
    background-color: white;
    box-shadow: 0 0 10px #8A2BE2; /* Optional: Add a subtle glow */
}
</style>
""", unsafe_allow_html=True)


# --- DATA LOADING ---
@st.cache_data
def load_all_data():
    # Load main dataset
    try:
        from pathlib import Path
        DATA_PATH = Path(__file__).parent / "data" / "Cleaned_Principal_Commodity_Exports_with_clusters.xlsx"
        df = pd.read_excel(DATA_PATH, engine='openpyxl')

        df['Cluster'] = 'Cluster ' + df['Cluster'].astype(str)
    except FileNotFoundError:
        st.error("Main data file not found. Please check the file path in the `load_all_data` function.")
        df = pd.DataFrame()

    # Load all analytical files
    try:
        risk_df = pd.read_csv("C:\\Users\\athar\\OneDrive\\Desktop\\College\\DS_ML_Analysis\\data\\market_risk_and_diversification.csv")
        gems_df = pd.read_csv("C:\\Users\\athar\\OneDrive\\Desktop\\College\\DS_ML_Analysis\\data\\hidden_gems.csv")
        sankey_df = pd.read_csv("C:\\Users\\athar\\OneDrive\\Desktop\\College\\DS_ML_Analysis\\data\\sankey_data.csv")
    except FileNotFoundError as e:
        st.error(f"An analytical file is missing: {e}. Please ensure all generated CSV files are present in the same directory as your app.py file.")
        risk_df, gems_df, sankey_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    return df, risk_df, gems_df, sankey_df

df, risk_df, gems_df, sankey_df = load_all_data()

# --- SIDEBAR (GLOBAL FILTERS) ---
with st.sidebar:
    st.title("Filters")
    st.markdown("Apply global filters to the entire dataset.")

    if not df.empty:
        selected_clusters = st.multiselect(
            "Filter by Cluster",
            options=sorted(df["Cluster"].unique()),
            default=sorted(df["Cluster"].unique())
        )
        min_val, max_val = float(df['VALUE_USD_MILLION'].min()), float(df['VALUE_USD_MILLION'].max())
        value_range = st.slider(
            "Filter by Value (USD Million)",
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val)
        )
    else:
        st.warning("Main data not loaded. Filters are unavailable.")
        selected_clusters = []
        value_range = (0,0)

    with st.expander("ℹ️ About this Dashboard"):
        st.info(
            """
            This dashboard provides an analysis of India's principal commodity exports for 2021-24.
            - **Data Source:** DGCI&S, Ministry of Commerce.
            - **Clusters:** Commodities are grouped using KMeans.
            - **New Features:** Includes Market Risk, Opportunity Finder, Treemap, and Sankey Diagram.
            """
        )

# Apply global filters first
if not df.empty:
    filtered_df = df[
        df["Cluster"].isin(selected_clusters) &
        df["VALUE_USD_MILLION"].between(value_range[0], value_range[1])
    ]
else:
    filtered_df = pd.DataFrame()


# --- MAIN PAGE ---
st.markdown(
    """
    <div class="top-bar">
        <span>Created by: Atharva Kale</span>
        <div>
            <a href="https://github.com/AtharvaKale1" target="_blank"><i class="fab fa-github"></i></a>
            <a href="https://www.linkedin.com/in/atharva-kale07/" target="_blank"><i class="fab fa-linkedin"></i></a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("📊📶🇮🇳 India's Export Data Intelligence Analysis")
st.markdown("Navigate through different analysis modes to uncover insights from India's 2021-24 export data.")

# --- DYNAMIC CONTROL PANEL ---
st.markdown("### 🚀 Select Your Analysis Mode")
analysis_mode = st.selectbox(
    "Choose how you want to explore the data:",
    [
        "📈 Dashboard Overview",
        "🌊 Export Flow Analysis",
        "🔬 Commodity Deep-Dive",
        "🌐 Geographic Comparison",
        "🧩 Cluster Explorer",
        "🎯 What-If Scenario Planner",
        "🌎 Market Risk & Diversification"
    ],
    label_visibility="collapsed"
)

# --- RENDER THE SELECTED PAGE ---

if analysis_mode == "📈 Dashboard Overview":
    st.markdown("#### Key Metrics Overview")

    row1_cols = st.columns(2)
    row1_cols[0].metric("Total Export Value", f"${filtered_df['VALUE_USD_MILLION'].sum():,.2f} M")
    row1_cols[1].metric("Total Quantity", f"${filtered_df['QUANTITY_KGS'].sum():,.0f} Kgs")

    row2_cols = st.columns(2)
    row2_cols[0].metric("Unique Commodities", f"{filtered_df['COMMODITY_NAME'].nunique()}")
    row2_cols[1].metric("Destination Countries", f"{filtered_df['COUNTRY'].nunique()}")

    st.markdown("---")

    st.markdown("#### Global Export Distribution by Value (USD Million)")
    country_df = filtered_df.groupby('COUNTRY')['VALUE_USD_MILLION'].sum().reset_index()

    if not country_df.empty and country_df['VALUE_USD_MILLION'].nunique() > 5:
        labels = ["Lowest", "Low", "Medium", "High", "Highest"]
        country_df['Value Tier'] = pd.qcut(country_df['VALUE_USD_MILLION'], q=5, labels=labels, duplicates='drop')

        color_map = {
            "Lowest": "#d1e5f0", "Low": "#92c5de", "Medium": "#4393c3",
            "High": "#2166ac", "Highest": "#053061"
        }

        fig_map = px.choropleth(
            country_df,
            locations="COUNTRY",
            locationmode="country names",
            color="Value Tier",
            hover_name="COUNTRY",
            hover_data={"Value Tier": False, "VALUE_USD_MILLION": ':.2f'},
            color_discrete_map=color_map,
            category_orders={"Value Tier": labels}
        )
        fig_map.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)'),
            margin={"r":0,"t":0,"l":0,"b":0},
            legend_title_text='Export Value Tier'
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Not enough data diversity to display a tiered world map. Please broaden your filters.")

    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### Top 15 Commodities by Export Value")
        top_commodities = filtered_df.groupby("COMMODITY_NAME")["VALUE_USD_MILLION"].sum().nlargest(15)
        fig = px.bar(top_commodities, x=top_commodities.values, y=top_commodities.index, orientation='h',
                     labels={'y': 'Commodity', 'x': 'Total Value (USD Million)'}, color=top_commodities.values, color_continuous_scale="Blues")
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Share of Value by Cluster")
        cluster_val = filtered_df.groupby("Cluster")["VALUE_USD_MILLION"].sum()
        fig_pie = px.pie(cluster_val, values=cluster_val.values, names=cluster_val.index, hole=0.5,
                         title="Total Value Distribution", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

elif analysis_mode == "🌊 Export Flow Analysis":
    st.markdown("#### 🌊 Export Value Flow (Sankey Diagram)")
    st.info("This diagram illustrates the flow of export revenue from a strategic **Cluster**, through its top **Commodities**, to its top **Destination Countries**.")

    if not sankey_df.empty:
        all_nodes = pd.unique(sankey_df[['source', 'target']].values.ravel('K'))
        node_dict = {node: i for i, node in enumerate(all_nodes)}

        sankey_df['source_id'] = sankey_df['source'].map(node_dict)
        sankey_df['target_id'] = sankey_df['target'].map(node_dict)

        fig = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=all_nodes),
            link=dict(source=sankey_df['source_id'], target=sankey_df['target_id'], value=sankey_df['value'])
        )])

        fig.update_layout(title_text="Top Export Value Flows", font_size=12, height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Sankey diagram data not available.")

elif analysis_mode == "🔬 Commodity Deep-Dive":
    st.markdown("#### Select a Commodity to Analyze in Detail")
    commodity_to_analyze = st.selectbox(
        "Search for a commodity",
        options=sorted(filtered_df["COMMODITY_NAME"].unique())
    )

    st.markdown("---")

    if commodity_to_analyze:
        commodity_df = filtered_df[filtered_df["COMMODITY_NAME"] == commodity_to_analyze]
        st.header(f"Analysis for: {commodity_to_analyze}")

        c_kpi_1, c_kpi_2, c_kpi_3 = st.columns(3)
        c_kpi_1.metric("Total Value", f"${commodity_df['VALUE_USD_MILLION'].sum():,.2f} M")
        c_kpi_2.metric("Avg. Price/Kg", f"${commodity_df['PRICE_PER_KG'].mean():.2f}")
        c_kpi_3.metric("Top Destination", commodity_df.loc[commodity_df['VALUE_USD_MILLION'].idxmax()]['COUNTRY'])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Top 10 Destinations by Value")
            top_countries = commodity_df.groupby("COUNTRY")["VALUE_USD_MILLION"].sum().nlargest(10)
            fig_country = px.bar(top_countries, x=top_countries.values, y=top_countries.index, orientation='h',
                                 color=top_countries.values, color_continuous_scale="Aggrnyl")
            fig_country.update_layout(yaxis={'categoryorder':'total ascending'}, title="Top Markets",
                                      xaxis_title="Value (USD M)", yaxis_title="Country")
            st.plotly_chart(fig_country, use_container_width=True)
        with col2:
            st.markdown("##### Price Distribution")
            fig_price_dist = px.histogram(commodity_df, x="PRICE_PER_KG", nbins=30,
                                          title="Distribution of Price per Kg")
            st.plotly_chart(fig_price_dist, use_container_width=True)

elif analysis_mode == "🌐 Geographic Comparison":
    st.markdown("#### Compare Export Performance Between Two Countries")

    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox("Select Country 1", options=sorted(filtered_df["COUNTRY"].unique()), index=0)
    with col2:
        country2 = st.selectbox("Select Country 2", options=sorted(filtered_df["COUNTRY"].unique()), index=1)

    st.markdown("---")

    if country1 and country2:
        df1 = filtered_df[filtered_df["COUNTRY"] == country1]
        df2 = filtered_df[filtered_df["COUNTRY"] == country2]

        total1 = df1['VALUE_USD_MILLION'].sum()
        total2 = df2['VALUE_USD_MILLION'].sum()

        st.header(f"Comparison: {country1} vs. {country2}")
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        comp_col1.metric(f"Total Value ({country1})", f"${total1:,.2f} M")
        comp_col2.metric(f"Total Value ({country2})", f"${total2:,.2f} M")
        comp_col3.metric("Value Difference", f"${total1 - total2:,.2f} M")

        st.markdown(f"##### Top Shared Commodities Exported to {country1} and {country2}")

        merged_df = pd.merge(df1, df2, on="COMMODITY_NAME", suffixes=(f'_{country1}', f'_{country2}'))
        merged_df['TOTAL_VALUE'] = merged_df[f'VALUE_USD_MILLION_{country1}'] + merged_df[f'VALUE_USD_MILLION_{country2}']

        if not merged_df.empty:
            top_shared = merged_df.nlargest(10, 'TOTAL_VALUE')
            fig = px.bar(top_shared, y='COMMODITY_NAME',
                         x=[f'VALUE_USD_MILLION_{country1}', f'VALUE_USD_MILLION_{country2}'],
                         title=f"Top 10 Shared Commodities by Value", barmode='group',
                         labels={'value': 'Export Value (USD M)', 'variable': 'Country'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No common commodities found between {country1} and {country2} with current filters.")

elif analysis_mode == "🧩 Cluster Explorer":
    st.markdown("#### Explore the Clusters")
    st.markdown("Clusters group commodities with similar value, quantity, and price profiles.")

    fig_scatter = px.scatter(
        filtered_df,
        x="QUANTITY_KGS",
        y="VALUE_USD_MILLION",
        color="Cluster",
        size="PRICE_PER_KG",
        hover_name="COMMODITY_NAME",
        hover_data=["COUNTRY"],
        log_x=True,
        log_y=True,
        title="Interactive Cluster Map (Log Scale)",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_scatter.update_layout(height=600)
    st.plotly_chart(fig_scatter, use_container_width=True)

elif analysis_mode == "🎯 What-If Scenario Planner":
    st.markdown("#### Scenario & Forecasting Tool")
    st.markdown("Select a commodity and adjust the sliders to forecast the potential impact on total export value.")

    commodity_options = sorted(filtered_df['COMMODITY_NAME'].unique())
    selected_commodity = st.selectbox("Select a Commodity to Analyze", commodity_options)

    if selected_commodity:
        st.markdown("##### Set Your Scenario Parameters")
        col1, col2 = st.columns(2)
        with col1:
            price_increase = st.slider("Price Increase (%)", 0, 100, 10)
        with col2:
            quantity_increase = st.slider("Quantity Increase (%)", 0, 100, 10)

        scenario_df = filtered_df[filtered_df['COMMODITY_NAME'] == selected_commodity].copy()
        current_total_value = scenario_df['VALUE_USD_MILLION'].sum()
        scenario_df['hypothetical_PRICE_PER_KG'] = scenario_df['PRICE_PER_KG'] * (1 + price_increase / 100)
        scenario_df['hypothetical_QUANTITY_KGS'] = scenario_df['QUANTITY_KGS'] * (1 + quantity_increase / 100)
        scenario_df['hypothetical_VALUE_USD_MILLION'] = (scenario_df['hypothetical_PRICE_PER_KG'] * scenario_df['hypothetical_QUANTITY_KGS']) / 1_000_000
        new_total_value = scenario_df['hypothetical_VALUE_USD_MILLION'].sum()
        uplift = new_total_value - current_total_value
        if current_total_value > 0:
            growth_percent = (uplift / current_total_value) * 100
        else:
            growth_percent = float('inf')

        st.markdown("---")
        st.markdown(f"#### Scenario Results for: **{selected_commodity}**")

        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Current Revenue", f"${current_total_value:,.2f} M")
        res_col2.metric("Hypothetical Revenue", f"${new_total_value:,.2f} M", f"${uplift:,.2f} M")
        res_col3.metric("Projected Growth", f"{growth_percent:.2f}%")

        fig = go.Figure(data=[
            go.Bar(name='Current Revenue', x=['Revenue'], y=[current_total_value], marker_color='rgba(255, 255, 255, 0.3)'),
            go.Bar(name='Hypothetical Revenue', x=['Revenue'], y=[new_total_value], marker_color='rgba(255, 255, 255, 0.7)')
        ])
        fig.update_layout(barmode='group', title_text='Revenue Comparison', yaxis_title="Value (USD Million)", template='plotly_dark', paper_bgcolor='#0d1b2a', plot_bgcolor='#0d1b2a', font_color='white')
        st.plotly_chart(fig, use_container_width=True)

elif analysis_mode == "🌎 Market Risk & Diversification":
    st.markdown("#### Market Concentration and Diversification Analysis")
    st.markdown("Identify commodities that are either well-diversified or at high risk due to dependence on a single market.")
    
    view_mode = st.radio("Select View", ["Most Diversified", "Highest Risk"], horizontal=True)

    if view_mode == "Most Diversified":
        st.markdown("##### 🌱 Top 15 Most Diversified Commodities")
        st.markdown("These commodities are exported to the highest number of unique countries, indicating a healthy and resilient market reach.")
        
        if not risk_df.empty:
            most_diversified = risk_df.sort_values(by="DIVERSIFICATION_SCORE", ascending=False).head(15)
            st.dataframe(most_diversified[['COMMODITY_NAME', 'DIVERSIFICATION_SCORE', 'TOTAL_COMMODITY_VALUE']], use_container_width=True)
        else:
            st.warning("Risk & Diversification data not available.")

    elif view_mode == "Highest Risk":
        st.markdown("##### ⚠️ Top 15 Highest-Risk Commodities (High Market Concentration)")
        st.markdown("These commodities are heavily reliant on a single country for a large percentage of their total export value.")

        if not risk_df.empty:
            highest_risk = risk_df.sort_values(by="CONCENTRATION_RISK_%", ascending=False).head(15)
            
            def style_risk(val):
                color = 'red' if val > 75 else ('orange' if val > 50 else 'green')
                return f'color: {color}; font-weight: bold;'
            
            st.dataframe(
                highest_risk[['COMMODITY_NAME', 'TOP_MARKET', 'CONCENTRATION_RISK_%']].style.applymap(
                    style_risk, subset=['CONCENTRATION_RISK_%']
                ).format({'CONCENTRATION_RISK_%': '{:.2f}%'}),
                use_container_width=True
            )
        else:
            st.warning("Risk & Diversification data not available.")


# --- DATA TABLE AT THE BOTTOM ---
if not filtered_df.empty:
    with st.expander("📂 View Filtered Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)

        @st.cache_data
        def convert_df_to_csv(df_to_convert):
            return df_to_convert.to_csv(index=False).encode('utf-8')

        csv = convert_df_to_csv(filtered_df)

        st.download_button(
           label="📥 Download data as CSV",
           data=csv,
           file_name='filtered_export_data.csv',
           mime='text/csv',
        )