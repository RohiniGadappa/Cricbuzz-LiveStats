# components/styles.py
# Custom CSS Styling Module
# Provides enhanced visual appeal for the Cricbuzz LiveStats dashboard

import streamlit as st
from config.app_config import AppConfig

def apply_custom_styles():
    """
    Apply custom CSS styles to enhance the visual appeal of the dashboard
    Following assignment requirements for professional presentation
    """
    
    st.markdown(f"""
    <style>
        /* Main Application Styling */
        .main-header {{
            background: {AppConfig.BACKGROUND_GRADIENT};
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .main-header h1 {{
            color: white;
            margin: 0;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .main-header h3 {{
            color: white;
            margin: 0;
            font-weight: 300;
            opacity: 0.9;
        }}
        
        .main-header p {{
            color: white;
            margin: 5px 0 0 0;
            opacity: 0.8;
            font-size: 14px;
        }}
        
        /* Card Components */
        .stat-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin: 10px 0;
            border: 1px solid #e9ecef;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        .metric-container {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            margin: 5px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        
        .metric-container h3 {{
            margin: 0;
            font-size: 1.5em;
            font-weight: 600;
        }}
        
        .metric-container p {{
            margin: 5px 0 0 0;
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        /* Sidebar Styling */
        .sidebar .sidebar-content {{
            background: linear-gradient(180deg, #2E86AB 0%, #A23B72 100%);
            color: white;
        }}
        
        .sidebar-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            color: white;
        }}
        
        /* Form Styling */
        .stSelectbox > div > div > div {{
            background-color: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            transition: border-color 0.3s ease;
        }}
        
        .stSelectbox > div > div > div:focus {{
            border-color: {AppConfig.PRIMARY_COLOR};
            box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.2);
        }}
        
        .stTextInput > div > div > input {{
            background-color: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            transition: border-color 0.3s ease;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {AppConfig.PRIMARY_COLOR};
            box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.2);
        }}
        
        .stNumberInput > div > div > input {{
            background-color: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
        }}
        
        /* Button Styling */
        .stButton > button {{
            background: linear-gradient(135deg, {AppConfig.PRIMARY_COLOR} 0%, {AppConfig.SECONDARY_COLOR} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        /* Table Styling */
        .dataframe {{
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .dataframe thead th {{
            background: linear-gradient(135deg, {AppConfig.PRIMARY_COLOR} 0%, {AppConfig.SECONDARY_COLOR} 100%);
            color: white;
            font-weight: 600;
            border: none;
        }}
        
        .dataframe tbody tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        .dataframe tbody tr:hover {{
            background-color: #e9ecef;
            transition: background-color 0.3s ease;
        }}
        
        /* Chart Container */
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
        }}
        
        /* Match Card Styling */
        .match-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }}
        
        .match-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        }}
        
        .match-status {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            display: inline-block;
            margin: 5px 0;
        }}
        
        .team-score {{
            font-size: 1.2em;
            font-weight: 600;
            color: #2c3e50;
            margin: 5px 0;
        }}
        
        .venue-info {{
            color: #6c757d;
            font-size: 0.9em;
            margin: 5px 0;
        }}
        
        /* Alert and Info Styling */
        .stAlert {{
            border-radius: 8px;
            border: none;
        }}
        
        .stInfo {{
            background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
            border-left: 4px solid #17a2b8;
        }}
        
        .stSuccess {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-left: 4px solid #28a745;
        }}
        
        .stWarning {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-left: 4px solid #ffc107;
        }}
        
        .stError {{
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border-left: 4px solid #dc3545;
        }}
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 5px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            padding: 10px 20px;
            background-color: transparent;
            border-radius: 8px;
            color: #6c757d;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {AppConfig.PRIMARY_COLOR} 0%, {AppConfig.SECONDARY_COLOR} 100%);
            color: white !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        
        /* Expander Styling */
        .streamlit-expanderHeader {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 8px;
            padding: 10px;
            font-weight: 600;
            color: #2c3e50;
            border: 1px solid #dee2e6;
        }}
        
        /* Code Block Styling */
        .stCode {{
            background: #2d3748;
            border-radius: 8px;
            border: 1px solid #4a5568;
        }}
        
        /* Metric Styling Enhancement */
        div[data-testid="metric-container"] {{
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 1px solid #e9ecef;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        
        div[data-testid="metric-container"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        /* Progress Bar Styling */
        .stProgress > div > div > div > div {{
            background: linear-gradient(135deg, {AppConfig.PRIMARY_COLOR} 0%, {AppConfig.SECONDARY_COLOR} 100%);
        }}
        
        /* Checkbox and Radio Styling */
        .stCheckbox > label > div {{
            border-radius: 4px;
        }}
        
        .stRadio > div > label > div {{
            border-radius: 50%;
        }}
        
        /* File Uploader Styling */
        .stFileUploader > div > div {{
            border: 2px dashed #e9ecef;
            border-radius: 8px;
            transition: border-color 0.3s ease;
        }}
        
        .stFileUploader > div > div:hover {{
            border-color: {AppConfig.PRIMARY_COLOR};
        }}
        
        /* Container Spacing */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .main-header {{
                padding: 15px;
            }}
            
            .stat-card {{
                padding: 15px;
                margin: 8px 0;
            }}
            
            .metric-container {{
                padding: 10px;
                margin: 3px;
            }}
        }}
        
        /* Loading Animation */
        .stSpinner > div {{
            border-top-color: {AppConfig.PRIMARY_COLOR} !important;
        }}
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, {AppConfig.PRIMARY_COLOR} 0%, {AppConfig.SECONDARY_COLOR} 100%);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, {AppConfig.SECONDARY_COLOR} 0%, {AppConfig.PRIMARY_COLOR} 100%);
        }}
        
        /* Custom Animation Classes */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(-20px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        .slide-in {{
            animation: slideIn 0.5s ease-out;
        }}
        
        /* Print Styles */
        @media print {{
            .main-header {{
                background: #f8f9fa !important;
                color: #2c3e50 !important;
                box-shadow: none !important;
            }}
            
            .stat-card {{
                box-shadow: none !important;
                border: 1px solid #dee2e6 !important;
            }}
        }}
        
        /* Dark Mode Support */
        @media (prefers-color-scheme: dark) {{
            .stat-card {{
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                border-color: #4a5568;
            }}
            
            .dataframe tbody tr:nth-child(even) {{
                background-color: #2d3748;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

def create_main_header():
    """
    Create the main dashboard header with gradient styling
    Reusable component for consistent header across pages
    """
    st.markdown(f"""
    <div class="main-header fade-in">
        <h1>{AppConfig.APP_ICON} {AppConfig.APP_TITLE}</h1>
        <h3>{AppConfig.APP_DESCRIPTION}</h3>
        <p>Domain: Sports Analytics | Skills: Python • SQL • Streamlit • JSON • REST API</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """
    Create a custom metric card with enhanced styling
    """
    delta_html = ""
    if delta:
        color = "#28a745" if delta_color == "normal" and str(delta).startswith("+") else "#dc3545" if str(delta).startswith("-") else "#6c757d"
        delta_html = f'<p style="color: {color}; margin: 5px 0 0 0; font-size: 0.9em;">{delta}</p>'
    
    return f"""
    <div class="metric-container slide-in">
        <h3>{value}</h3>
        <p>{title}</p>
        {delta_html}
    </div>
    """

def create_stat_card(content):
    """
    Create a styled card for statistics and content
    """
    return f"""
    <div class="stat-card fade-in">
        {content}
    </div>
    """

def create_match_card(match_data):
    """
    Create a styled match card with team information
    """
    return f"""
    <div class="match-card fade-in">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div class="team-score">{match_data.get('team1', 'Team 1')}</div>
            <div style="text-align: center;">
                <strong>VS</strong>
                <div class="match-status">{match_data.get('status', 'Live')}</div>
            </div>
            <div class="team-score">{match_data.get('team2', 'Team 2')}</div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <div>{match_data.get('team1_score', 'N/A')}</div>
            <div>{match_data.get('team2_score', 'N/A')}</div>
        </div>
        <div class="venue-info">
            <strong>Venue:</strong> {match_data.get('venue', 'Unknown')}
        </div>
        <div class="venue-info">
            <strong>Format:</strong> {match_data.get('format', 'Unknown')}
        </div>
    </div>
    """

def display_metric_cards(metrics_data):
    """
    Display metrics in attractive cards using custom styling
    """
    cols = st.columns(len(metrics_data))
    for i, (title, value, delta) in enumerate(metrics_data):
        with cols[i]:
            st.markdown(
                create_metric_card(title, value, delta),
                unsafe_allow_html=True
            )

def create_loading_animation():
    """
    Create a custom loading animation
    """
    return """
    <div style="display: flex; justify-content: center; align-items: center; height: 100px;">
        <div class="loading-spinner">
            <div style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #FF6B35; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        </div>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """

def create_success_message(message):
    """
    Create a styled success message
    """
    return f"""
    <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                border-left: 4px solid #28a745; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 10px 0;
                animation: fadeIn 0.5s ease-in;">
        <strong>✅ Success:</strong> {message}
    </div>
    """

def create_error_message(message):
    """
    Create a styled error message
    """
    return f"""
    <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                border-left: 4px solid #dc3545; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 10px 0;
                animation: fadeIn 0.5s ease-in;">
        <strong>❌ Error:</strong> {message}
    </div>
    """

def create_info_message(message):
    """
    Create a styled info message
    """
    return f"""
    <div style="background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); 
                border-left: 4px solid #17a2b8; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 10px 0;
                animation: fadeIn 0.5s ease-in;">
        <strong>ℹ️ Info:</strong> {message}
    </div>
    """

def apply_chart_styling():
    """
    Return consistent chart styling configuration for Plotly charts
    """
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': '#2c3e50', 'family': 'Arial, sans-serif'},
        'colorway': [AppConfig.PRIMARY_COLOR, AppConfig.SECONDARY_COLOR, AppConfig.ACCENT_COLOR, '#28a745', '#ffc107', '#dc3545'],
        'title': {'font': {'size': 18, 'color': '#2c3e50'}},
        'xaxis': {'gridcolor': '#e9ecef', 'linecolor': '#dee2e6'},
        'yaxis': {'gridcolor': '#e9ecef', 'linecolor': '#dee2e6'}
    }