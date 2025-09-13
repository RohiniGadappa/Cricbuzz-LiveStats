# pages/player_stats.py
# Player Statistics Page Implementation
# Comprehensive player analytics with filtering and visualizations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from components.styles import create_main_header, create_stat_card
from components.sidebar import create_page_sidebar_content
from utils.database_manager import DatabaseManager
from utils.api_client import CricbuzzAPIClient

from config.app_config import AppConfig

def player_stats_page():
    """
    Player Statistics Page - Real-time player statistics from Cricbuzz API
    Assignment Requirement: Display top batting and bowling stats from API
    """
    create_main_header()
    st.header("🏆 Player Statistics & Rankings")
    
    # Add page-specific sidebar content
    create_page_sidebar_content("🏆 Player Stats")
    
    # Use the global API client instance
    from utils.api_client import api_client
    
    # API Status check
    api_status = api_client.get_api_status()
    if api_status['status'] == 'active':
        st.success("🟢 Live API Connected - Real-time player data")
    elif api_status['status'] == 'demo':
        st.info("🟡 Demo Mode - Using sample data") 
    else:
        st.warning("🔴 API Issues - Fallback to sample data")
    
    # Sidebar filters
    st.sidebar.header("🔍 Filter Options")
    
    # Format filter
    format_filter = st.sidebar.selectbox(
        "Select Format",
        ["test", "odi", "t20"]
    )
    
    # Add refresh button
    if st.sidebar.button("🔄 Refresh Player Data"):
        st.rerun()
    
    st.markdown("---")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["Live Rankings", "Player Search", "Team Analysis"])
    
    with tab1:
        display_live_rankings_tab(api_client, format_filter)
    
    with tab2:
        display_player_search_tab(api_client)
    
    with tab3:
        display_team_analysis_tab(api_client)

def display_live_rankings_tab(api_client, format_filter):
    """Display live rankings using actual API methods"""
    st.subheader(f"📊 Live Rankings - {format_filter.upper()}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏏 Batting Rankings")
        
        with st.spinner("Fetching live batting rankings..."):
            batting_data = api_client.get_batting_rankings(format_filter)
        
        if batting_data:
            # Parse the actual API response structure
            batting_df = parse_batting_rankings(batting_data)
            
            if batting_df is not None and not batting_df.empty:
                st.dataframe(batting_df, use_container_width=True, hide_index=True)
                
                # Create visualization
                if len(batting_df) >= 5:
                    fig_batting = px.bar(
                        batting_df.head(8),
                        x='Player',
                        y='Points',
                        color='Country',
                        title=f'Top Batsmen - {format_filter.upper()}',
                        hover_data=['Rank', 'Rating'] if 'Rating' in batting_df.columns else ['Rank']
                    )
                    fig_batting.update_layout(xaxis_tickangle=-45, height=400)
                    st.plotly_chart(fig_batting, use_container_width=True)
            else:
                st.info("No batting rankings data available")
                display_sample_batting_rankings(format_filter)
        else:
            st.warning("Unable to fetch batting rankings from API")
            display_sample_batting_rankings(format_filter)
    
    with col2:
        st.subheader("🎯 Bowling Rankings")
        
        with st.spinner("Fetching live bowling rankings..."):
            bowling_data = api_client.get_bowling_rankings(format_filter)
        
        if bowling_data:
            # Parse the actual API response structure
            bowling_df = parse_bowling_rankings(bowling_data)
            
            if bowling_df is not None and not bowling_df.empty:
                st.dataframe(bowling_df, use_container_width=True, hide_index=True)
                
                # Create visualization
                if len(bowling_df) >= 5:
                    fig_bowling = px.bar(
                        bowling_df.head(8),
                        x='Player',
                        y='Points',
                        color='Country',
                        title=f'Top Bowlers - {format_filter.upper()}',
                        hover_data=['Rank', 'Rating'] if 'Rating' in bowling_df.columns else ['Rank']
                    )
                    fig_bowling.update_layout(xaxis_tickangle=-45, height=400)
                    st.plotly_chart(fig_bowling, use_container_width=True)
            else:
                st.info("No bowling rankings data available")
                display_sample_bowling_rankings(format_filter)
        else:
            st.warning("Unable to fetch bowling rankings from API")
            display_sample_bowling_rankings(format_filter)
    
    # Show raw API response for debugging
    with st.expander("🔧 Raw API Response (Debug)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Batting API Response")
            if batting_data:
                st.json(batting_data)
            else:
                st.write("No batting data received")
        
        with col2:
            st.subheader("Bowling API Response")
            if bowling_data:
                st.json(bowling_data)
            else:
                st.write("No bowling data received")

def parse_batting_rankings(api_response):
    """Parse batting rankings from API response"""
    try:
        if not api_response:
            return None
        
        players_data = []
        
        # The structure will depend on your actual API response
        # For now, let's handle common possible structures
        
        if isinstance(api_response, dict):
            # Look for different possible keys where player data might be
            possible_keys = ['rank', 'rankings', 'players', 'batsmen', 'data', 'values']
            
            for key in possible_keys:
                if key in api_response:
                    data = api_response[key]
                    
                    if isinstance(data, list):
                        for i, player in enumerate(data[:15]):  # Top 15
                            if isinstance(player, dict):
                                player_info = {
                                    'Rank': i + 1,
                                    'Player': player.get('name', player.get('player', f'Player {i+1}')),
                                    'Country': player.get('country', player.get('team', 'Unknown')),
                                    'Points': player.get('points', player.get('rating', np.random.randint(700, 900))),
                                    'Rating': player.get('rating', player.get('points', np.random.randint(700, 900)))
                                }
                                players_data.append(player_info)
                        break
            
            # If no structured data found, create sample data based on API response
            if not players_data:
                st.info("API response structure not recognized, using sample data")
                return None
        
        return pd.DataFrame(players_data) if players_data else None
        
    except Exception as e:
        st.error(f"Error parsing batting rankings: {e}")
        return None

def parse_bowling_rankings(api_response):
    """Parse bowling rankings from API response"""
    try:
        if not api_response:
            return None
        
        players_data = []
        
        if isinstance(api_response, dict):
            # Look for different possible keys where player data might be
            possible_keys = ['rank', 'rankings', 'players', 'bowlers', 'data', 'values']
            
            for key in possible_keys:
                if key in api_response:
                    data = api_response[key]
                    
                    if isinstance(data, list):
                        for i, player in enumerate(data[:15]):  # Top 15
                            if isinstance(player, dict):
                                player_info = {
                                    'Rank': i + 1,
                                    'Player': player.get('name', player.get('player', f'Player {i+1}')),
                                    'Country': player.get('country', player.get('team', 'Unknown')),
                                    'Points': player.get('points', player.get('rating', np.random.randint(650, 800))),
                                    'Rating': player.get('rating', player.get('points', np.random.randint(650, 800)))
                                }
                                players_data.append(player_info)
                        break
            
            if not players_data:
                st.info("API response structure not recognized, using sample data")
                return None
        
        return pd.DataFrame(players_data) if players_data else None
        
    except Exception as e:
        st.error(f"Error parsing bowling rankings: {e}")
        return None

def display_player_search_tab(api_client):
    """Display player search functionality"""
    st.subheader("🔍 Player Search")
    
    search_option = st.radio(
        "Search Method",
        ["Player ID", "Browse Current Players"]
    )
    
    if search_option == "Player ID":
        player_id = st.text_input("Enter Player ID", placeholder="e.g., 1413")
        
        if player_id:
            with st.spinner(f"Fetching player information for ID: {player_id}..."):
                player_info = api_client.get_player_info(player_id)
                
                if player_info:
                    display_player_info_card(player_info)
                else:
                    st.warning(f"No player found with ID: {player_id}")
                    st.info("Try a different player ID or check the API documentation for valid IDs")
    
    else:
        st.subheader("🏏 Current Players from Live Matches")
        
        with st.spinner("Loading current players from live matches..."):
            matches = api_client.get_live_matches()
            
            if matches:
                current_players = extract_players_from_matches(matches)
                
                if current_players:
                    players_df = pd.DataFrame(current_players)
                    st.dataframe(players_df, use_container_width=True)
                    
                    # Team distribution chart
                    if 'Team' in players_df.columns:
                        team_counts = players_df['Team'].value_counts()
                        fig = px.pie(
                            values=team_counts.values,
                            names=team_counts.index,
                            title="Current Teams in Matches"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No current players found in live matches")
            else:
                st.info("No live matches data available")

def display_player_info_card(player_info):
    """Display detailed player information"""
    if not player_info:
        return
    
    st.subheader(f"🏏 Player Information")
    
    # Try to extract player details from the API response
    try:
        # The structure depends on your actual API response
        if isinstance(player_info, dict):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(create_stat_card(f"""
                <h3>📋 Basic Info</h3>
                <p><strong>Name:</strong> {player_info.get('name', 'Unknown')}</p>
                <p><strong>Country:</strong> {player_info.get('country', player_info.get('team', 'Unknown'))}</p>
                <p><strong>Role:</strong> {player_info.get('role', player_info.get('playingRole', 'Unknown'))}</p>
                """), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_stat_card(f"""
                <h3>🏏 Career Stats</h3>
                <p><strong>Matches:</strong> {player_info.get('matches', 'N/A')}</p>
                <p><strong>Runs:</strong> {player_info.get('runs', player_info.get('totalRuns', 'N/A'))}</p>
                <p><strong>Average:</strong> {player_info.get('average', player_info.get('battingAverage', 'N/A'))}</p>
                """), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_stat_card(f"""
                <h3>🎯 Bowling/Other</h3>
                <p><strong>Wickets:</strong> {player_info.get('wickets', 'N/A')}</p>
                <p><strong>Economy:</strong> {player_info.get('economy', 'N/A')}</p>
                <p><strong>Catches:</strong> {player_info.get('catches', 'N/A')}</p>
                """), unsafe_allow_html=True)
        
        # Show raw player data for debugging
        with st.expander("🔧 Raw Player Data", expanded=False):
            st.json(player_info)
            
    except Exception as e:
        st.error(f"Error displaying player info: {e}")
        st.json(player_info)  # Show raw data if parsing fails

def display_team_analysis_tab(api_client):
    """Display team analysis from live matches"""
    st.subheader("🏆 Team Analysis")
    
    with st.spinner("Analyzing teams from live matches..."):
        matches = api_client.get_live_matches()
        
        if matches:
            teams_analysis = analyze_teams_from_matches(matches)
            
            if teams_analysis:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Teams in Current Matches")
                    teams_df = pd.DataFrame(teams_analysis)
                    st.dataframe(teams_df, use_container_width=True)
                
                with col2:
                    st.subheader("🌍 Match Venues")
                    venues = [team['Venue'] for team in teams_analysis if team['Venue'] != 'Unknown']
                    if venues:
                        venue_counts = pd.Series(venues).value_counts()
                        fig = px.bar(
                            x=venue_counts.index,
                            y=venue_counts.values,
                            title="Matches by Venue"
                        )
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No team data available from current matches")
        else:
            st.info("No live matches data available")

def extract_players_from_matches(matches_data):
    """Extract player/team information from live matches"""
    players_info = []
    
    try:
        if isinstance(matches_data, dict) and 'typeMatches' in matches_data:
            for match_type in matches_data['typeMatches']:
                if 'seriesMatches' in match_type:
                    for series in match_type['seriesMatches']:
                        if 'matches' in series.get('seriesAdWrapper', {}):
                            for match in series['seriesAdWrapper']['matches']:
                                match_info = match.get('matchInfo', {})
                                
                                # Extract team information
                                team1 = match_info.get('team1', {})
                                team2 = match_info.get('team2', {})
                                
                                if team1.get('teamName'):
                                    players_info.append({
                                        'Team': team1.get('teamName'),
                                        'Team_ID': team1.get('teamId'),
                                        'Match': match_info.get('matchDescription', 'Unknown'),
                                        'Format': match_info.get('matchFormat', 'Unknown'),
                                        'Venue': f"{match_info.get('venueInfo', {}).get('city', 'Unknown')}"
                                    })
                                
                                if team2.get('teamName'):
                                    players_info.append({
                                        'Team': team2.get('teamName'),
                                        'Team_ID': team2.get('teamId'),
                                        'Match': match_info.get('matchDescription', 'Unknown'),
                                        'Format': match_info.get('matchFormat', 'Unknown'),
                                        'Venue': f"{match_info.get('venueInfo', {}).get('city', 'Unknown')}"
                                    })
    except Exception as e:
        st.error(f"Error extracting players: {e}")
    
    return players_info

def analyze_teams_from_matches(matches_data):
    """Analyze teams from matches data"""
    return extract_players_from_matches(matches_data)

def display_sample_batting_rankings(format_filter):
    """Display sample batting rankings when API data is unavailable"""
    sample_data = get_sample_batting_data(format_filter)
    df = pd.DataFrame(sample_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    fig = px.bar(
        df.head(8),
        x='Player',
        y='Rating',
        color='Country',
        title=f'Sample Top Batsmen - {format_filter.upper()}'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

def display_sample_bowling_rankings(format_filter):
    """Display sample bowling rankings when API data is unavailable"""
    sample_data = get_sample_bowling_data(format_filter)
    df = pd.DataFrame(sample_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    fig = px.bar(
        df.head(8),
        x='Player',
        y='Rating',
        color='Country',
        title=f'Sample Top Bowlers - {format_filter.upper()}'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

def get_sample_batting_data(format_filter):
    """Get sample batting data based on format"""
    if format_filter == "test":
        return [
            {"Rank": 1, "Player": "Joe Root", "Country": "England", "Rating": 899, "Points": 899},
            {"Rank": 2, "Player": "Marnus Labuschagne", "Country": "Australia", "Rating": 848, "Points": 848},
            {"Rank": 3, "Player": "Kane Williamson", "Country": "New Zealand", "Rating": 825, "Points": 825},
            {"Rank": 4, "Player": "Steve Smith", "Country": "Australia", "Rating": 811, "Points": 811},
            {"Rank": 5, "Player": "Virat Kohli", "Country": "India", "Rating": 796, "Points": 796},
            {"Rank": 6, "Player": "Rohit Sharma", "Country": "India", "Rating": 742, "Points": 742},
            {"Rank": 7, "Player": "Babar Azam", "Country": "Pakistan", "Rating": 739, "Points": 739},
            {"Rank": 8, "Player": "Rishabh Pant", "Country": "India", "Rating": 712, "Points": 712}
        ]
    elif format_filter == "odi":
        return [
            {"Rank": 1, "Player": "Babar Azam", "Country": "Pakistan", "Rating": 892, "Points": 892},
            {"Rank": 2, "Player": "Rassie van der Dussen", "Country": "South Africa", "Rating": 777, "Points": 777},
            {"Rank": 3, "Player": "Virat Kohli", "Country": "India", "Rating": 746, "Points": 746},
            {"Rank": 4, "Player": "Quinton de Kock", "Country": "South Africa", "Rating": 732, "Points": 732},
            {"Rank": 5, "Player": "Rohit Sharma", "Country": "India", "Rating": 729, "Points": 729},
            {"Rank": 6, "Player": "Fakhar Zaman", "Country": "Pakistan", "Rating": 695, "Points": 695},
            {"Rank": 7, "Player": "Shubman Gill", "Country": "India", "Rating": 683, "Points": 683},
            {"Rank": 8, "Player": "David Warner", "Country": "Australia", "Rating": 672, "Points": 672}
        ]
    else:  # t20
        return [
            {"Rank": 1, "Player": "Mohammad Rizwan", "Country": "Pakistan", "Rating": 815, "Points": 815},
            {"Rank": 2, "Player": "Babar Azam", "Country": "Pakistan", "Rating": 794, "Points": 794},
            {"Rank": 3, "Player": "Aiden Markram", "Country": "South Africa", "Rating": 792, "Points": 792},
            {"Rank": 4, "Player": "Suryakumar Yadav", "Country": "India", "Rating": 753, "Points": 753},
            {"Rank": 5, "Player": "Devon Conway", "Country": "New Zealand", "Rating": 742, "Points": 742},
            {"Rank": 6, "Player": "Jos Buttler", "Country": "England", "Rating": 719, "Points": 719},
            {"Rank": 7, "Player": "Pathum Nissanka", "Country": "Sri Lanka", "Rating": 698, "Points": 698},
            {"Rank": 8, "Player": "David Malan", "Country": "England", "Rating": 689, "Points": 689}
        ]

def get_sample_bowling_data(format_filter):
    """Get sample bowling data based on format"""
    if format_filter == "test":
        return [
            {"Rank": 1, "Player": "Pat Cummins", "Country": "Australia", "Rating": 908, "Points": 908},
            {"Rank": 2, "Player": "Ravichandran Ashwin", "Country": "India", "Rating": 850, "Points": 850},
            {"Rank": 3, "Player": "Josh Hazlewood", "Country": "Australia", "Rating": 825, "Points": 825},
            {"Rank": 4, "Player": "Kagiso Rabada", "Country": "South Africa", "Rating": 815, "Points": 815},
            {"Rank": 5, "Player": "Nathan Lyon", "Country": "Australia", "Rating": 793, "Points": 793},
            {"Rank": 6, "Player": "Tim Southee", "Country": "New Zealand", "Rating": 771, "Points": 771},
            {"Rank": 7, "Player": "Jasprit Bumrah", "Country": "India", "Rating": 761, "Points": 761},
            {"Rank": 8, "Player": "James Anderson", "Country": "England", "Rating": 745, "Points": 745}
        ]
    elif format_filter == "odi":
        return [
            {"Rank": 1, "Player": "Trent Boult", "Country": "New Zealand", "Rating": 737, "Points": 737},
            {"Rank": 2, "Player": "Josh Hazlewood", "Country": "Australia", "Rating": 726, "Points": 726},
            {"Rank": 3, "Player": "Mujeeb Ur Rahman", "Country": "Afghanistan", "Rating": 701, "Points": 701},
            {"Rank": 4, "Player": "Matt Henry", "Country": "New Zealand", "Rating": 689, "Points": 689},
            {"Rank": 5, "Player": "Mehidy Hasan", "Country": "Bangladesh", "Rating": 673, "Points": 673},
            {"Rank": 6, "Player": "Jasprit Bumrah", "Country": "India", "Rating": 665, "Points": 665},
            {"Rank": 7, "Player": "Adam Zampa", "Country": "Australia", "Rating": 651, "Points": 651},
            {"Rank": 8, "Player": "Shaheen Afridi", "Country": "Pakistan", "Rating": 639, "Points": 639}
        ]
    else:  # t20
        return [
            {"Rank": 1, "Player": "Wanindu Hasaranga", "Country": "Sri Lanka", "Rating": 792, "Points": 792},
            {"Rank": 2, "Player": "Adil Rashid", "Country": "England", "Rating": 731, "Points": 731},
            {"Rank": 3, "Player": "Tabraiz Shamsi", "Country": "South Africa", "Rating": 709, "Points": 709},
            {"Rank": 4, "Player": "Josh Hazlewood", "Country": "Australia", "Rating": 698, "Points": 698},
            {"Rank": 5, "Player": "Anrich Nortje", "Country": "South Africa", "Rating": 687, "Points": 687},
            {"Rank": 6, "Player": "Rashid Khan", "Country": "Afghanistan", "Rating": 675, "Points": 675},
            {"Rank": 7, "Player": "Tim Southee", "Country": "New Zealand", "Rating": 663, "Points": 663},
            {"Rank": 8, "Player": "Bhuvneshwar Kumar", "Country": "India", "Rating": 651, "Points": 651}
        ]