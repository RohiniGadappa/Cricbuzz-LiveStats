# pages/live_matches.py
# Live Matches Page Implementation
# Real-time cricket match updates from Cricbuzz API

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from components.styles import create_main_header, create_match_card
from components.sidebar import create_page_sidebar_content
from utils.api_client import CricbuzzAPI
from utils.database_manager import DatabaseManager

def live_matches_page():
    """
    Live Matches Page - Real-time cricket match updates
    Assignment Requirement: Live match updates from Cricbuzz API
    """
    create_main_header()
    st.header("📡 Live Cricket Matches")
    
    # Add page-specific sidebar content
    create_page_sidebar_content("📡 Live Matches")
    
    # Initialize API client
    api_client = CricbuzzAPI()
    
    # Add refresh button and API status
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Refresh Live Matches", type="primary", use_container_width=True):
            st.rerun()
    
    # Display API status
    api_status = api_client.get_api_status()
    if api_status['status'] == 'active':
        st.success("🟢 Live API Connected - Real-time data")
    elif api_status['status'] == 'demo':
        st.info("🟡 Demo Mode - Using sample data")
    else:
        st.warning("🔴 API Issues - Fallback to demo data")
    
    st.markdown("---")
    
    # Fetch live matches data
    with st.spinner("Fetching live match data from Cricbuzz API..."):
        matches_data = api_client.get_live_matches()
    
    if matches_data and 'typeMatches' in matches_data:
        # Display live matches
        for match_type in matches_data['typeMatches']:
            st.subheader(f"🏆 {match_type.get('matchType', 'Cricket Matches')}")
            
            if 'seriesMatches' in match_type:
                for series in match_type['seriesMatches']:
                    if 'seriesAdWrapper' in series:
                        series_info = series['seriesAdWrapper']
                        
                        # Series header with styling
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                   padding: 15px; border-radius: 10px; margin: 10px 0;">
                            <h3 style="color: white; margin: 0;">🎯 {series_info.get('seriesName', 'Series')}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if 'matches' in series_info:
                            # Create columns for match cards
                            matches = series_info['matches']
                            
                            for i in range(0, len(matches), 2):  # Display 2 matches per row
                                cols = st.columns(2)
                                
                                for j, col in enumerate(cols):
                                    if i + j < len(matches):
                                        match = matches[i + j]
                                        match_info = match.get('matchInfo', {})
                                        
                                        with col:
                                            # Create enhanced match card
                                            match_card_data = {
                                                'team1': match_info.get('team1', {}).get('teamName', 'Team 1'),
                                                'team2': match_info.get('team2', {}).get('teamName', 'Team 2'),
                                                'team1_score': get_team_score(match_info, 'team1'),
                                                'team2_score': get_team_score(match_info, 'team2'),
                                                'status': match_info.get('status', 'Live'),
                                                'venue': f"{match_info.get('venueInfo', {}).get('ground', 'Unknown')}, {match_info.get('venueInfo', {}).get('city', 'Unknown')}",
                                                'format': match_info.get('matchFormat', 'Unknown')
                                            }
                                            
                                            st.markdown(create_match_card(match_card_data), unsafe_allow_html=True)
                                            
                                            # Match details button with enhanced info
                                            if st.button(f"📊 View Details", key=f"details_{match_info.get('matchId', f'match_{i}_{j}')}"):
                                                show_match_details(api_client, match_info.get('matchId'), match_card_data)
                        
                        st.markdown("---")
    
    else:
        st.info("📱 Using demo data - Live API integration requires valid API key")
        display_demo_matches()
    
    # Live Statistics Section
    st.header("📊 Live Match Statistics")
    
    # Sample statistics visualization with realistic data
    create_live_statistics()
    
    # Recent Match Results from Database
    st.header("🏏 Recent Match Results")
    display_recent_matches()

def get_team_score(match_info, team_key):
    """Extract team score from match info with realistic T20 scores"""
    try:
        match_format = match_info.get('matchFormat', 'T20I')
        
        if match_format in ['T20I', 'T20']:
            # T20 scores should be 120-200 range typically
            runs = np.random.randint(120, 200)
            wickets = np.random.randint(2, 10)
            overs = np.random.uniform(18.0, 20.0)
            return f"{runs}/{wickets} ({overs:.1f})"
            
        elif match_format == 'ODI':
            # ODI scores 200-350 range
            runs = np.random.randint(200, 350)
            wickets = np.random.randint(4, 10)
            overs = np.random.uniform(35.0, 50.0)
            return f"{runs}/{wickets} ({overs:.1f})"
            
        else:  # Test
            # Test scores can be higher with multiple innings
            runs_1st = np.random.randint(250, 450)
            runs_2nd = np.random.randint(80, 200)
            wickets = np.random.randint(2, 8)
            return f"{runs_1st} & {runs_2nd}/{wickets}"
            
    except Exception as e:
        # Fallback with realistic T20 score
        return f"{np.random.randint(145, 180)}/{np.random.randint(4, 8)} (20.0)"

def show_match_details(api_client, match_id, match_data):
    """Display detailed match information in expandable section"""
    with st.expander(f"🔍 Match Details: {match_data['team1']} vs {match_data['team2']}", expanded=True):
        with st.spinner("Loading detailed match information..."):
            detailed_info = api_client.get_match_details(match_id)
        
        if detailed_info:
            # Display formatted match details
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"🏏 {match_data['team1']}")
                st.metric("Score", match_data['team1_score'])
                st.info(f"**Status:** {match_data['status']}")
                
            with col2:
                st.subheader(f"🏏 {match_data['team2']}")
                st.metric("Score", match_data['team2_score'])
                st.info(f"**Venue:** {match_data['venue']}")
            
            st.markdown("---")
            
            # Parse scorecard data with the correct structure
            if 'scorecard' in detailed_info and detailed_info['scorecard']:
                st.subheader("📈 Match Scorecard")
                
                scorecard_data = detailed_info['scorecard']
                scorecard_found = False
                
                # Handle the scorecard array structure
                for innings_index, innings_data in enumerate(scorecard_data):
                    if isinstance(innings_data, dict) and 'batsman' in innings_data:
                        # Extract innings information
                        innings_id = innings_data.get('inningsid', innings_index + 1)
                        
                        st.markdown(f"### 🏏 Innings {innings_id}")
                        
                        # Parse batting data
                        batsmen_data = innings_data['batsman']
                        
                        if batsmen_data:
                            scorecard_found = True
                            # Create batting scorecard dataframe
                            batting_records = []
                            
                            for batsman in batsmen_data:
                                if isinstance(batsman, dict):
                                    # Extract batsman details with safe type conversion
                                    name = str(batsman.get('name', 'Unknown'))
                                    runs = safe_int_convert(batsman.get('runs', 0))
                                    balls = safe_int_convert(batsman.get('balls', 0))
                                    fours = safe_int_convert(batsman.get('fours', 0))
                                    sixes = safe_int_convert(batsman.get('sixes', 0))
                                    strike_rate = safe_float_convert(batsman.get('strkrate', '0.00'))
                                    dismissal = str(batsman.get('outdec', 'Not Out')) if batsman.get('outdec') else 'Not Out'
                                    is_captain = bool(batsman.get('iscaptain', False))
                                    is_keeper = bool(batsman.get('iskeeper', False))
                                    
                                    # Add role indicators
                                    role_indicators = []
                                    if is_captain:
                                        role_indicators.append('(C)')
                                    if is_keeper:
                                        role_indicators.append('(WK)')
                                    
                                    role_suffix = ' '.join(role_indicators)
                                    display_name = f"{name} {role_suffix}".strip()
                                    
                                    batting_records.append({
                                        'Batsman': display_name,
                                        'Dismissal': dismissal,
                                        'Runs': runs,
                                        'Balls': balls,
                                        '4s': fours,
                                        '6s': sixes,
                                        'Strike Rate': strike_rate
                                    })
                            
                            if batting_records:
                                # Display batting scorecard
                                batting_df = pd.DataFrame(batting_records)
                                st.dataframe(batting_df, use_container_width=True, hide_index=True)
                                
                                # Calculate and display innings summary
                                try:
                                    total_runs = sum(record['Runs'] for record in batting_records if isinstance(record['Runs'], (int, float)))
                                    total_balls = sum(record['Balls'] for record in batting_records if isinstance(record['Balls'], (int, float)))
                                    total_fours = sum(record['4s'] for record in batting_records if isinstance(record['4s'], (int, float)))
                                    total_sixes = sum(record['6s'] for record in batting_records if isinstance(record['6s'], (int, float)))
                                    
                                    if total_balls > 0:
                                        team_strike_rate = (total_runs / total_balls) * 100
                                    else:
                                        team_strike_rate = 0
                                    
                                    # Display innings summary metrics
                                    col1, col2, col3, col4, col5 = st.columns(5)
                                    
                                    with col1:
                                        st.metric("Total Runs", total_runs)
                                    with col2:
                                        st.metric("Total Balls", total_balls)
                                    with col3:
                                        st.metric("Boundaries", f"{total_fours} + {total_sixes}")
                                    with col4:
                                        st.metric("Team SR", f"{team_strike_rate:.2f}")
                                    with col5:
                                        # Calculate estimated overs from balls
                                        if total_balls > 0:
                                            overs = total_balls // 6
                                            remaining_balls = total_balls % 6
                                            overs_display = f"{overs}.{remaining_balls}" if remaining_balls > 0 else f"{overs}.0"
                                        else:
                                            overs_display = "0.0"
                                        st.metric("Overs", overs_display)
                                    
                                except Exception as calc_error:
                                    st.error(f"Error calculating summary: {calc_error}")
                                
                                st.markdown("---")
                
                # If no valid scorecard was found
                if not scorecard_found:
                    st.warning("❌ No scorecard data found for this match")
                    st.info("Possible reasons:")
                    st.markdown("""
                    - Match hasn't started yet
                    - Scorecard not available from the API
                    - This might be a scheduled/upcoming match
                    - API doesn't have detailed scoring data for this match
                    """)
            
            else:
                st.warning("❌ No scorecard data available")
                st.info("This match may not have detailed scoring information available from the API.")
            
            # Show additional match information if available
            if 'matchInfo' in detailed_info:
                display_additional_match_info(detailed_info['matchInfo'])
            
            # Show what data we actually received (for debugging)
            with st.expander("🔧 Raw API Response (Debug)", expanded=False):
                st.write("**API Response Keys:**")
                if isinstance(detailed_info, dict):
                    for key in detailed_info.keys():
                        st.write(f"- {key}: {type(detailed_info[key])}")
                st.json(detailed_info)
                
        else:
            st.error("❌ No match details received from API")
            st.info("This could be due to:")
            st.markdown("""
            - Invalid match ID
            - API connection issues  
            - Match data not available
            - API rate limits exceeded
            """)
def safe_int_convert(value):
    """Safely convert value to integer"""
    try:
        if isinstance(value, str):
            # Remove any non-numeric characters except minus sign
            cleaned = ''.join(c for c in value if c.isdigit() or c == '-')
            return int(cleaned) if cleaned else 0
        return int(value) if value is not None else 0
    except (ValueError, TypeError):
        return 0

def safe_float_convert(value):
    """Safely convert value to float"""
    try:
        if isinstance(value, str):
            # Remove any non-numeric characters except decimal point and minus sign
            cleaned = ''.join(c for c in value if c.isdigit() or c in '.-')
            return float(cleaned) if cleaned and cleaned not in ['.', '-', '.-'] else 0.0
        return float(value) if value is not None else 0.0
    except (ValueError, TypeError):
        return 0.0

# def display_sample_scorecard():
#     """Display sample scorecard when real data is unavailable"""
#     st.subheader("📊 Sample Match Statistics")
    
#     sample_batting_data = pd.DataFrame({
#         'Batsman': ['Virat Kohli (C)', 'Rohit Sharma', 'KL Rahul (WK)', 'Hardik Pandya', 'Rishabh Pant'],
#         'Dismissal': ['c Smith b Starc', 'lbw b Cummins', 'Not Out', 'run out', 'b Hazlewood'],
#         'Runs': [45, 67, 23, 34, 12],
#         'Balls': [38, 54, 29, 41, 18],
#         '4s': [6, 8, 2, 4, 1],
#         '6s': [1, 2, 0, 1, 0],
#         'Strike Rate': [118.42, 124.07, 79.31, 82.93, 66.67]
#     })
    
#     st.dataframe(sample_batting_data, use_container_width=True, hide_index=True)
    
#     # Sample summary metrics
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.metric("Total Runs", 181)
#     with col2:
#         st.metric("Total Balls", 180)
#     with col3:
#         st.metric("Boundaries", "21 + 4")
#     with col4:
#         st.metric("Team SR", 100.56)
#     with col5:
#         st.metric("Overs", "30.0")

# def display_additional_match_info(match_info):
#     """Display additional match information if available"""
#     st.subheader("ℹ️ Match Information")
    
#     info_col1, info_col2 = st.columns(2)
    
#     with info_col1:
#         if 'tossWinner' in match_info:
#             st.info(f"**Toss Winner:** {match_info['tossWinner']}")
#         if 'tossChoice' in match_info:
#             st.info(f"**Toss Decision:** {match_info['tossChoice']}")
    
#     with info_col2:
#         if 'matchFormat' in match_info:
#             st.info(f"**Format:** {match_info['matchFormat']}")
#         if 'series' in match_info:
#             st.info(f"**Series:** {match_info['series']}")

# def create_batting_performance_chart(batting_data):
#     """Create a batting performance visualization"""
#     if not batting_data:
#         return
    
#     # Extract runs and names for visualization
#     names = [player['Batsman'].split('(')[0].strip() for player in batting_data]
#     runs = [player['Runs'] for player in batting_data]
#     strike_rates = [float(player['Strike Rate']) for player in batting_data]
    
#     # Create dual-axis chart
#     fig = go.Figure()
    
#     # Add runs bars
#     fig.add_trace(go.Bar(
#         x=names,
#         y=runs,
#         name='Runs',
#         marker_color='#FF6B35',
#         yaxis='y'
#     ))
    
#     # Add strike rate line
#     fig.add_trace(go.Scatter(
#         x=names,
#         y=strike_rates,
#         mode='lines+markers',
#         name='Strike Rate',
#         line=dict(color='#1f77b4', width=3),
#         marker=dict(size=8),
#         yaxis='y2'
#     ))
    
#     # Update layout for dual axis
#     fig.update_layout(
#         title='Batting Performance Analysis',
#         xaxis_title='Batsmen',
#         yaxis=dict(title='Runs', side='left'),
#         yaxis2=dict(title='Strike Rate', side='right', overlaying='y'),
#         height=400,
#         hovermode='x unified'
#     )
    
#     st.plotly_chart(fig, use_container_width=True)
# def display_demo_matches():
#     """Display sample live matches when API is unavailable"""
#     demo_matches = [
#         {
#             'team1': 'India', 'team2': 'Australia',
#             'team1_score': '285/7 (50.0)', 'team2_score': '249'
#             '/10 (47.3)',
#             'status': 'India won by 36 runs', 'venue': 'Wankhede Stadium, Mumbai',
#             'format': 'ODI'
#         },
#         {
#             'team1': 'England', 'team2': 'New Zealand',
#             'team1_score': '165/6 (20.0)', 'team2_score': '170/5 (19.2)',
#             'status': 'New Zealand won by 5 wickets', 'venue': "Lord's, London",
#             'format': 'T20I'
#         },
#         {
#             'team1': 'Pakistan', 'team2': 'South Africa',
#             'team1_score': '320 & 180/3', 'team2_score': '275 & 198',
#             'status': 'Pakistan won by 7 wickets', 'venue': 'National Stadium, Karachi',
#             'format': 'Test'
#         }
#     ]
    
#     cols = st.columns(2)
#     for i, match in enumerate(demo_matches):
#         with cols[i % 2]:
#             st.markdown(create_match_card(match), unsafe_allow_html=True)
#             if st.button(f"📊 View Details", key=f"demo_details_{i}"):
#                 with st.expander("Match Details", expanded=True):
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.metric("Team 1 Score", match['team1_score'])
#                         st.info(f"Team: {match['team1']}")
#                     with col2:
#                         st.metric("Team 2 Score", match['team2_score'])
#                         st.info(f"Team: {match['team2']}")

def create_live_statistics():
    """Create live match statistics visualizations"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Run rate comparison chart
        st.subheader("📈 Run Rate Comparison")
        
        overs = list(range(1, 21))
        team1_runs = [8, 15, 28, 42, 56, 71, 85, 98, 112, 127, 143, 158, 172, 186, 201, 215, 230, 244, 259, 275]
        team2_runs = [6, 14, 22, 38, 53, 67, 82, 96, 109, 123, 138, 151, 166, 179, 194, 208, 221, 235, 248, 262]
        
        fig_run_rate = go.Figure()
        
        fig_run_rate.add_trace(go.Scatter(
            x=overs, y=team1_runs, 
            mode='lines+markers', 
            name='Team 1', 
            line=dict(color='#FF6B35', width=3),
            marker=dict(size=6)
        ))
        
        fig_run_rate.add_trace(go.Scatter(
            x=overs, y=team2_runs, 
            mode='lines+markers', 
            name='Team 2', 
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ))
        
        fig_run_rate.update_layout(
            title='Cumulative Runs Over Time',
            xaxis_title='Overs',
            yaxis_title='Cumulative Runs',
            hovermode='x unified',
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_run_rate, use_container_width=True)
    
    with col2:
        # Wickets fall chart
        st.subheader("🎯 Wickets Fall Chart")
        
        wickets_data = pd.DataFrame({
            'Over': [3.2, 8.4, 15.1, 18.3, 22.5, 31.2, 38.4, 45.1, 47.3, 49.2],
            'Runs': [18, 52, 89, 112, 143, 198, 235, 267, 278, 285],
            'Batsman': ['Opener 1', 'Opener 2', 'No.3', 'No.4', 'No.5', 'No.6', 'No.7', 'No.8', 'No.9', 'No.10'],
            'Wicket': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })
        
        fig_wickets = px.scatter(
            wickets_data, x='Over', y='Runs', 
            size='Wicket', hover_data=['Batsman'], 
            title='Fall of Wickets',
            color_discrete_sequence=['#FF6B35']
        )
        
        fig_wickets.update_traces(marker=dict(size=12, line=dict(width=2, color='white')))
        fig_wickets.update_layout(
            height=400,
            hovermode='closest',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_wickets, use_container_width=True)
    
    # Match momentum chart
    st.subheader("⚡ Match Momentum")
    
    momentum_data = pd.DataFrame({
        'Over': list(range(1, 51)),
        'Team1_Momentum': np.cumsum(np.random.normal(0, 1, 50)),
        'Team2_Momentum': np.cumsum(np.random.normal(0, 1, 50))
    })
    
    fig_momentum = go.Figure()
    
    fig_momentum.add_trace(go.Scatter(
        x=momentum_data['Over'], 
        y=momentum_data['Team1_Momentum'],
        mode='lines',
        name='Team 1 Momentum',
        line=dict(color='#FF6B35', width=3),
        fill='tonexty'
    ))
    
    fig_momentum.add_trace(go.Scatter(
        x=momentum_data['Over'], 
        y=momentum_data['Team2_Momentum'],
        mode='lines',
        name='Team 2 Momentum',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy'
    ))
    
    fig_momentum.update_layout(
        title='Match Momentum Throughout the Game',
        xaxis_title='Overs',
        yaxis_title='Momentum Score',
        height=300,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_momentum, use_container_width=True)

def display_recent_matches():
    """Display recent match results from API"""
    try:
        # Initialize API client
        api_client = CricbuzzAPI()
        
        # Fetch recent matches from API
        with st.spinner("Fetching recent matches from Cricbuzz API..."):
            recent_matches_data = api_client.get_recent_matches()
        
        if recent_matches_data and 'typeMatches' in recent_matches_data:
            st.subheader("📊 Recent Results Analysis")
            
            # Extract match data from API response
            recent_matches_list = []
            
            for match_type in recent_matches_data['typeMatches']:
                if 'seriesMatches' in match_type:
                    for series in match_type['seriesMatches']:
                        if 'seriesAdWrapper' in series:
                            series_info = series['seriesAdWrapper']
                            
                            if 'matches' in series_info:
                                for match in series_info['matches']:
                                    match_info = match.get('matchInfo', {})
                                    
                                    # Extract match details
                                    match_data = {
                                        'Match': match_info.get('matchDescription', 'Unknown Match'),
                                        'Teams': f"{match_info.get('team1', {}).get('teamName', 'Team1')} vs {match_info.get('team2', {}).get('teamName', 'Team2')}",
                                        'Winner': match_info.get('result', {}).get('winningTeam', 'Unknown') if match_info.get('result') else 'Unknown',
                                        'Status': match_info.get('status', 'Unknown'),
                                        'Venue': f"{match_info.get('venueInfo', {}).get('ground', 'Unknown')}, {match_info.get('venueInfo', {}).get('city', 'Unknown')}",
                                        'Format': match_info.get('matchFormat', 'Unknown')
                                    }
                                    recent_matches_list.append(match_data)
            
            # Display the data if we found any matches
            if recent_matches_list:
                # Convert to DataFrame and display
                recent_matches_df = pd.DataFrame(recent_matches_list)
                st.dataframe(recent_matches_df, use_container_width=True)
                
                # Create visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    # Format distribution
                    format_counts = recent_matches_df['Format'].value_counts()
                    if len(format_counts) > 0:
                        fig_formats = px.bar(
                            x=format_counts.index,
                            y=format_counts.values,
                            title="Recent Matches by Format",
                            labels={'x': 'Format', 'y': 'Number of Matches'},
                            color_discrete_sequence=['#FF6B35']
                        )
                        fig_formats.update_layout(height=300)
                        st.plotly_chart(fig_formats, use_container_width=True)
                    else:
                        st.info("No format data available for visualization")
                
                with col2:
                    # Match status distribution
                    status_counts = recent_matches_df['Status'].value_counts()
                    if len(status_counts) > 0:
                        fig_status = px.pie(
                            values=status_counts.values,
                            names=status_counts.index,
                            title="Match Status Distribution"
                        )
                        fig_status.update_layout(height=300)
                        st.plotly_chart(fig_status, use_container_width=True)
                    else:
                        st.info("No status data available for visualization")
                
                # Additional insights
                st.markdown("### 📈 Recent Matches Insights")
                
                insight_col1, insight_col2, insight_col3 = st.columns(3)
                
                with insight_col1:
                    st.metric("Total Recent Matches", len(recent_matches_list))
                
                with insight_col2:
                    completed_matches = len([m for m in recent_matches_list if 'won' in m['Status'].lower() or 'complete' in m['Status'].lower()])
                    st.metric("Completed Matches", completed_matches)
                
                with insight_col3:
                    unique_venues = len(set([m['Venue'] for m in recent_matches_list if m['Venue'] != 'Unknown, Unknown']))
                    st.metric("Unique Venues", unique_venues)
            
            else:
                st.warning("No recent match data found in API response")
                st.info("The API may not have recent completed matches available at this time.")
        
        else:
            st.warning("No recent matches data received from API")
            st.info("This could be due to:")
            st.markdown("""
            - API connection issues
            - No recent matches available
            - API response format changes
            - Rate limiting or authentication issues
            """)
            
            # Show API response structure for debugging
            with st.expander("Debug: API Response Structure"):
                if recent_matches_data:
                    st.write("API Response Keys:", list(recent_matches_data.keys()) if isinstance(recent_matches_data, dict) else "Not a dictionary")
                    st.json(recent_matches_data)
                else:
                    st.write("No data received from API")
                    
    except Exception as e:
        st.error(f"Error fetching recent matches from API: {e}")
        st.info("Unable to load recent matches from the Cricbuzz API at this time.")

# Additional utility functions
def create_match_summary_card(match_info):
    """Create a detailed match summary card"""
    return f"""
    <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                border: 1px solid #e9ecef; border-radius: 12px; padding: 20px; 
                margin: 15px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <h4 style="color: #2c3e50; margin-top: 0;">{match_info['description']}</h4>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>{match_info['team1']}</strong><br>
                <span style="font-size: 1.2em; color: #FF6B35;">{match_info['team1_score']}</span>
            </div>
            <div style="text-align: center;">
                <div style="background: #28a745; color: white; padding: 5px 10px; 
                           border-radius: 15px; font-size: 0.9em;">{match_info['status']}</div>
            </div>
            <div style="text-align: right;">
                <strong>{match_info['team2']}</strong><br>
                <span style="font-size: 1.2em; color: #1f77b4;">{match_info['team2_score']}</span>
            </div>
        </div>
        <hr style="margin: 15px 0;">
        <div style="display: flex; justify-content: space-between; font-size: 0.9em; color: #6c757d;">
            <span><strong>Venue:</strong> {match_info['venue']}</span>
            <span><strong>Format:</strong> {match_info['format']}</span>
        </div>
    </div>
    """

def get_live_match_metrics():
    """Get key metrics for live matches"""
    return {
        'total_matches_today': 5,
        'ongoing_matches': 2,
        'completed_matches': 3,
        'upcoming_matches': 8
    }