# Business Analysis Dashboard

A comprehensive Streamlit dashboard for analyzing marketing performance and business metrics across multiple platforms.

## Features

- **Multi-Platform Analytics**: Facebook, Google, and TikTok campaign performance
- **Key Performance Indicators**: ROAS, CAC, CTR, and CPC metrics
- **Interactive Filtering**: Filter by date range, platform, and geographic location
- **Visual Analytics**: Charts for channel performance, spend distribution, and trends

## Live Demo

**[View Dashboard](https://business-analysis-dashboard.streamlit.app)**

## Data Structure

The dashboard expects the following CSV files:
- `Facebook.csv` - Facebook campaign data
- `Google.csv` - Google Ads campaign data  
- `TikTok.csv` - TikTok campaign data
- `business.csv` - Overall business metrics

## Technologies Used

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Deployment**: Streamlit Community Cloud

## Metrics Tracked

- **Marketing Spend**: Total advertising investment
- **Attributed Revenue**: Revenue directly linked to marketing efforts
- **ROAS**: Return on Advertising Spend
- **CAC**: Customer Acquisition Cost
- **CTR**: Click-Through Rate
- **CPC**: Cost Per Click

