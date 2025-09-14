import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    layout="wide"
)

# CSS with light teal background - multiple selectors to ensure it works
st.markdown("""
<style>
    .main > div { background-color: #bff0f2 !important; }
    .block-container { background-color: #bff0f2 !important; }
    .main .block-container { background-color: #bff0f2 !important; }
    [data-testid="stAppViewContainer"] { background-color: #bff0f2 !important; }
    [data-testid="stHeader"] { background-color: #bff0f2 !important; }
    .stApp { background-color: #bff0f2 !important; }
    .metric-container { background-color: #f8e8e8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; }
    .insight-box { background-color: #f5e8e8; padding: 1rem; border-left: 4px solid #1f77b4; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)  # Cache for only 60 seconds to help with debugging
def load_data():
    """Load marketing and business data"""
    try:
        # Load actual files
        dfs = []
        for platform, file in [('Facebook', 'Facebook.csv'), ('Google', 'Google.csv'), ('TikTok', 'TikTok.csv')]:
            df = pd.read_csv(file)
            df['platform'] = platform
            dfs.append(df)
        
        marketing_df = pd.concat(dfs, ignore_index=True)
        business_df = pd.read_csv('Business.csv')
        
    except FileNotFoundError as e:
        # Sample data
        st.warning(f"CSV files not found. Error: {e}. Using sample data.")
        dates = pd.date_range(start='2025-05-16', periods=120, freq='D')
        
        # Marketing data
        marketing_data = []
        for date in dates:
            for platform in ['Facebook', 'Google', 'TikTok']:
                impressions = np.random.randint(50000, 200000)
                clicks = np.random.randint(1000, 5000)
                spend = np.random.uniform(500, 3000)
                
                marketing_data.append({
                    'date': date, 'platform': platform,
                    'tactic': np.random.choice(['ASC', 'Retargeting', 'Search']),
                    'state': np.random.choice(['NY', 'CA', 'TX', 'FL']),
                    'impression': impressions, 'clicks': clicks, 'spend': spend,
                    'attributed revenue': spend * np.random.uniform(1.5, 4.0)
                })
        
        marketing_df = pd.DataFrame(marketing_data)
        
        # Business data
        business_data = []
        for date in dates:
            revenue = np.random.uniform(20000, 40000)
            business_data.append({
                'date': date,
                '# of orders': np.random.randint(200, 400),
                'new customers': np.random.randint(40, 120),
                'total revenue': revenue,
                'gross profit': revenue * np.random.uniform(0.4, 0.6)
            })
        
        business_df = pd.DataFrame(business_data)
    
    # Convert dates and calculate metrics
    marketing_df['date'] = pd.to_datetime(marketing_df['date'])
    business_df['date'] = pd.to_datetime(business_df['date'])
    
    # Safe calculations
    marketing_df['roas'] = marketing_df['attributed revenue'] / marketing_df['spend'].replace(0, 1)
    marketing_df['ctr'] = (marketing_df['clicks'] / marketing_df['impression'].replace(0, 1)) * 100
    marketing_df['cpc'] = marketing_df['spend'] / marketing_df['clicks'].replace(0, 1)
    
    return marketing_df, business_df

def calculate_kpis(marketing_df, business_df):
    """Calculate KPIs"""
    if marketing_df.empty:
        return {'total_spend': 0, 'total_attributed_revenue': 0, 'overall_roas': 0, 'blended_cac': 0}
    
    total_spend = marketing_df['spend'].sum()
    total_attributed_revenue = marketing_df['attributed revenue'].sum()
    total_new_customers = business_df['new customers'].sum() if not business_df.empty else 0
    
    return {
        'total_spend': total_spend,
        'total_attributed_revenue': total_attributed_revenue,
        'overall_roas': total_attributed_revenue / total_spend if total_spend > 0 else 0,
        'blended_cac': total_spend / total_new_customers if total_new_customers > 0 else 0
    }

def create_channel_chart(marketing_df):
    """Create channel performance chart"""
    if marketing_df.empty:
        return None, pd.DataFrame()
        
    stats = marketing_df.groupby('platform').agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'clicks': 'sum',
        'impression': 'sum'
    }).reset_index()
    
    stats['roas'] = stats['attributed revenue'] / stats['spend']
    stats['ctr'] = (stats['clicks'] / stats['impression']) * 100
    
    # Simple bar chart for ROAS
    fig = px.bar(stats, x='platform', y='roas', 
                 title='ROAS by Channel',
                 color='roas', color_continuous_scale='Blues')
    
    return fig, stats

def create_spend_distribution_chart(marketing_df):
    """Create spend distribution pie chart"""
    if marketing_df.empty:
        return None
        
    spend_by_platform = marketing_df.groupby('platform')['spend'].sum().reset_index()
    
    fig = px.pie(spend_by_platform, values='spend', names='platform',
                 title='Marketing Spend Distribution by Platform')
    
    return fig

def main():
    st.title("Marketing Intelligence Dashboard")
    
    # Load data
    marketing_df, business_df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date filter
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(marketing_df['date'].min().date(), marketing_df['date'].max().date())
    )
    
    # Platform filter
    platforms = st.sidebar.multiselect(
        "Platforms",
        options=marketing_df['platform'].unique(),
        default=marketing_df['platform'].unique()
    )
    
    # State filter
    states = st.sidebar.multiselect(
        "States",
        options=marketing_df['state'].unique(),
        default=marketing_df['state'].unique()
    )
    
    # Filter data
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_marketing = marketing_df[
            (marketing_df['date'] >= start_date) &
            (marketing_df['date'] <= end_date) &
            (marketing_df['platform'].isin(platforms)) &
            (marketing_df['state'].isin(states))
        ]
        filtered_business = business_df[
            (business_df['date'] >= start_date) &
            (business_df['date'] <= end_date)
        ]
    else:
        filtered_marketing, filtered_business = marketing_df, business_df
    
    # KPIs
    kpis = calculate_kpis(filtered_marketing, filtered_business)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Marketing Spend", f"${kpis['total_spend']:,.0f}")
    with col2:
        st.metric("Attributed Revenue", f"${kpis['total_attributed_revenue']:,.0f}")
    with col3:
        st.metric("ROAS", f"{kpis['overall_roas']:.2f}x")
    with col4:
        st.metric("CAC", f"${kpis['blended_cac']:.0f}")
    
    # Channel Performance
    st.header("Channel Performance")
    chart, stats = create_channel_chart(filtered_marketing)
    
    if chart is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(chart, use_container_width=True)
        with col2:
            spend_chart = create_spend_distribution_chart(filtered_marketing)
            if spend_chart:
                st.plotly_chart(spend_chart, use_container_width=True)
        
        st.dataframe(stats.round(2))
    
    # Simple trend chart
    if not filtered_marketing.empty:
        st.header("Performance Trends")
        daily_data = filtered_marketing.groupby('date').agg({
            'spend': 'sum',
            'attributed revenue': 'sum'
        }).reset_index()
        
        fig = px.line(daily_data, x='date', y=['spend', 'attributed revenue'],
                      title='Daily Spend vs Revenue')
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
