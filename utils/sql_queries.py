# utils/sql_queries.py
# SQL Queries Module - Implementation of all 25 assignment questions
# Organized by difficulty level as per assignment requirements

import pandas as pd
import streamlit as st
from utils.database_manager import DatabaseManager

class SQLQueries:
    """
    SQL Queries Class - Implementation of all 25 assignment questions
    Organized by difficulty level as per assignment requirements
    """
    
    def __init__(self, db_manager):
        """Initialize with database manager instance"""
        self.db = db_manager
    
    # ==========================================================================
    # BEGINNER LEVEL QUERIES (Questions 1-8)
    # Basic SELECT, WHERE, GROUP BY, ORDER BY operations
    # ==========================================================================
    
    def query_1_indian_players(self):
        """Question 1: Find all players who represent India"""
        query = """
        SELECT 
            name as 'Player Name', 
            playing_role as 'Playing Role', 
            batting_style as 'Batting Style', 
            bowling_style as 'Bowling Style'
        FROM players 
        WHERE country = 'India'
        ORDER BY name
        """
        return self._execute_query(query, "Indian Players")
    
    def query_2_recent_matches(self):
        """Question 2: Show matches played in last 30 days"""
        query = """
        SELECT 
            match_description as 'Match Description',
            team1 || ' vs ' || team2 as 'Teams',
            venue_name || ', ' || venue_city as 'Venue',
            match_date as 'Match Date'
        FROM matches 
        WHERE match_date >= date('now', '-30 days')
        ORDER BY match_date DESC
        """
        return self._execute_query(query, "Recent Matches (Last 30 Days)")
    
    def query_3_top_run_scorers(self):
        """Question 3: Top 10 highest run scorers in ODI"""
        query = """
        SELECT 
            name as 'Player Name',
            total_runs as 'Total Runs',
            batting_average as 'Batting Average',
            centuries as 'Centuries'
        FROM players 
        WHERE total_runs > 0
        ORDER BY total_runs DESC
        LIMIT 10
        """
        return self._execute_query(query, "Top 10 Run Scorers")
    
    def query_4_large_venues(self):
        """Question 4: Venues with capacity > 50,000"""
        query = """
        SELECT DISTINCT 
            venue_name as 'Venue Name',
            venue_city as 'City',
            venue_country as 'Country',
            venue_capacity as 'Capacity'
        FROM matches 
        WHERE venue_capacity > 50000
        ORDER BY venue_capacity DESC
        """
        return self._execute_query(query, "Large Venues (50,000+ Capacity)")
    
    def query_5_team_wins(self):
        """Question 5: Count wins for each team"""
        query = """
        SELECT 
            winning_team as 'Team',
            COUNT(*) as 'Total Wins'
        FROM matches 
        WHERE winning_team IS NOT NULL
        GROUP BY winning_team
        ORDER BY COUNT(*) DESC
        """
        return self._execute_query(query, "Team Win Statistics")
    
    def query_6_players_by_role(self):
        """Question 6: Count players by playing role"""
        query = """
        SELECT 
            playing_role as 'Playing Role',
            COUNT(*) as 'Number of Players'
        FROM players 
        GROUP BY playing_role
        ORDER BY COUNT(*) DESC
        """
        return self._execute_query(query, "Players by Role")
    
    def query_7_highest_scores_by_format(self):
        """Question 7: Highest individual scores by format"""
        query = """
        SELECT 
            m.match_format as 'Format',
            MAX(pp.runs_scored) as 'Highest Individual Score'
        FROM matches m
        JOIN player_performances pp ON m.id = pp.match_id
        WHERE pp.runs_scored > 0
        GROUP BY m.match_format
        ORDER BY MAX(pp.runs_scored) DESC
        """
        return self._execute_query(query, "Highest Scores by Format")
    
    def query_8_series_2024(self):
        """Question 8: Cricket series that started in 2024"""
        query = """
        SELECT 
            series_name as 'Series Name',
            host_country as 'Host Country',
            match_type as 'Match Type',
            start_date as 'Start Date',
            total_matches as 'Total Matches'
        FROM series 
        WHERE strftime('%Y', start_date) = '2024'
        ORDER BY start_date DESC
        """
        return self._execute_query(query, "Cricket Series Starting in 2024")
    
    # ==========================================================================
    # INTERMEDIATE LEVEL QUERIES (Questions 9-16)
    # JOINs, Subqueries, Advanced filtering, CASE statements
    # ==========================================================================
    
    def query_9_allrounders(self):
        """Question 9: All-rounders with 1000+ runs and 50+ wickets"""
        query = """
        SELECT 
            name as 'Player Name',
            total_runs as 'Total Runs',
            wickets_taken as 'Total Wickets',
            'All Formats' as 'Cricket Format'
        FROM players 
        WHERE playing_role = 'All-rounder' 
        AND total_runs > 1000 
        AND wickets_taken > 50
        ORDER BY total_runs DESC
        """
        return self._execute_query(query, "Elite All-Rounders")
    
    def query_10_completed_matches(self):
        """Question 10: Last 20 completed matches details"""
        query = """
        SELECT 
            match_description as 'Match Description',
            team1 || ' vs ' || team2 as 'Teams',
            winning_team as 'Winner',
            victory_margin as 'Victory Margin',
            victory_type as 'Victory Type',
            venue_name as 'Venue'
        FROM matches 
        WHERE winning_team IS NOT NULL
        ORDER BY match_date DESC
        LIMIT 20
        """
        return self._execute_query(query, "Last 20 Completed Matches")
    
    def query_11_format_comparison(self):
        """Question 11: Player performance across formats"""
        query = """
        SELECT 
            p.name as 'Player Name',
            SUM(CASE WHEN m.match_format = 'Test' THEN pp.runs_scored ELSE 0 END) as 'Test Runs',
            SUM(CASE WHEN m.match_format = 'ODI' THEN pp.runs_scored ELSE 0 END) as 'ODI Runs',
            SUM(CASE WHEN m.match_format = 'T20I' THEN pp.runs_scored ELSE 0 END) as 'T20I Runs',
            ROUND(AVG(pp.runs_scored), 2) as 'Overall Average'
        FROM players p
        JOIN player_performances pp ON p.id = pp.player_id
        JOIN matches m ON pp.match_id = m.id
        GROUP BY p.name
        HAVING COUNT(DISTINCT m.match_format) >= 2
        ORDER BY AVG(pp.runs_scored) DESC
        """
        return self._execute_query(query, "Multi-Format Player Performance")
    
    def query_12_home_away_analysis(self):
        """Question 12: Team performance - Home vs Away"""
        query = """
        SELECT 
            winning_team as 'Team',
            SUM(CASE WHEN venue_country = 
                CASE 
                    WHEN winning_team = 'India' THEN 'India'
                    WHEN winning_team = 'Australia' THEN 'Australia'
                    WHEN winning_team = 'England' THEN 'England'
                    WHEN winning_team = 'New Zealand' THEN 'New Zealand'
                    WHEN winning_team = 'Pakistan' THEN 'Pakistan'
                    WHEN winning_team = 'South Africa' THEN 'South Africa'
                    ELSE venue_country
                END THEN 1 ELSE 0 END) as 'Home Wins',
            SUM(CASE WHEN venue_country != 
                CASE 
                    WHEN winning_team = 'India' THEN 'India'
                    WHEN winning_team = 'Australia' THEN 'Australia'
                    WHEN winning_team = 'England' THEN 'England'
                    WHEN winning_team = 'New Zealand' THEN 'New Zealand'
                    WHEN winning_team = 'Pakistan' THEN 'Pakistan'
                    WHEN winning_team = 'South Africa' THEN 'South Africa'
                    ELSE venue_country
                END THEN 1 ELSE 0 END) as 'Away Wins'
        FROM matches 
        WHERE winning_team IS NOT NULL
        GROUP BY winning_team
        ORDER BY (COUNT(*)) DESC
        """
        return self._execute_query(query, "Home vs Away Performance")
    
    def query_13_partnerships(self):
        """Question 13: High-scoring partnerships"""
        query = """
        SELECT 
            p1.name as 'Batsman 1',
            p2.name as 'Batsman 2',
            (pp1.runs_scored + pp2.runs_scored) as 'Partnership Runs',
            m.match_description as 'Match'
        FROM player_performances pp1
        JOIN player_performances pp2 ON pp1.match_id = pp2.match_id 
            AND pp2.batting_position = pp1.batting_position + 1
        JOIN players p1 ON pp1.player_id = p1.id
        JOIN players p2 ON pp2.player_id = p2.id
        JOIN matches m ON pp1.match_id = m.id
        WHERE (pp1.runs_scored + pp2.runs_scored) >= 100
        ORDER BY (pp1.runs_scored + pp2.runs_scored) DESC
        """
        return self._execute_query(query, "Century Partnerships")
    
    def query_14_venue_bowling(self):
        """Question 14: Bowling performance at venues"""
        query = """
        SELECT 
            p.name as 'Bowler',
            m.venue_name as 'Venue',
            ROUND(AVG(CAST(pp.runs_conceded AS FLOAT) / NULLIF(pp.overs_bowled, 0)), 2) as 'Avg Economy',
            SUM(pp.wickets_taken) as 'Total Wickets',
            COUNT(*) as 'Matches Played'
        FROM players p
        JOIN player_performances pp ON p.id = pp.player_id
        JOIN matches m ON pp.match_id = m.id
        WHERE p.playing_role IN ('Bowler', 'All-rounder')
        AND m.match_format IN ('ODI', 'T20I')
        AND pp.overs_bowled >= 2
        GROUP BY p.name
        HAVING COUNT(*) >= 3 AND AVG(pp.overs_bowled) >= 2
        ORDER BY AVG(CAST(pp.runs_conceded AS FLOAT) / NULLIF(pp.overs_bowled, 0))
        LIMIT 10
        """
        return self._execute_query(query, "Most Economical Bowlers (Limited Overs)")
    
    def query_19_consistent_batsmen(self):
        """Question 19: Most consistent batsmen (low standard deviation)"""
        query = """
        SELECT 
            p.name as 'Batsman',
            ROUND(AVG(pp.runs_scored), 2) as 'Average Runs',
            COUNT(*) as 'Innings',
            ROUND(
                SQRT(
                    AVG(pp.runs_scored * pp.runs_scored) - 
                    (AVG(pp.runs_scored) * AVG(pp.runs_scored))
                ), 2
            ) as 'Standard Deviation (Lower = More Consistent)'
        FROM players p
        JOIN player_performances pp ON p.id = pp.player_id
        JOIN matches m ON pp.match_id = m.id
        WHERE pp.balls_faced >= 10 
        AND m.match_date >= '2022-01-01'
        AND p.playing_role IN ('Batsman', 'All-rounder', 'Wicket-keeper')
        GROUP BY p.name
        HAVING COUNT(*) >= 3
        ORDER BY SQRT(
            AVG(pp.runs_scored * pp.runs_scored) - 
            (AVG(pp.runs_scored) * AVG(pp.runs_scored))
        )
        LIMIT 10
        """
        return self._execute_query(query, "Most Consistent Batsmen (2022+)")
    
    def query_20_format_experience(self):
        """Question 20: Player experience across formats"""
        query = """
        SELECT 
            p.name as 'Player',
            SUM(CASE WHEN m.match_format = 'Test' THEN 1 ELSE 0 END) as 'Test Matches',
            SUM(CASE WHEN m.match_format = 'ODI' THEN 1 ELSE 0 END) as 'ODI Matches',
            SUM(CASE WHEN m.match_format = 'T20I' THEN 1 ELSE 0 END) as 'T20I Matches',
            ROUND(AVG(CASE WHEN m.match_format = 'Test' THEN pp.runs_scored END), 2) as 'Test Avg',
            ROUND(AVG(CASE WHEN m.match_format = 'ODI' THEN pp.runs_scored END), 2) as 'ODI Avg',
            ROUND(AVG(CASE WHEN m.match_format = 'T20I' THEN pp.runs_scored END), 2) as 'T20I Avg',
            COUNT(*) as 'Total Matches'
        FROM players p
        JOIN player_performances pp ON p.id = pp.player_id
        JOIN matches m ON pp.match_id = m.id
        GROUP BY p.name
        HAVING COUNT(*) >= 3
        ORDER BY COUNT(*) DESC
        """
        return self._execute_query(query, "Multi-Format Experience")
    
    def query_21_performance_ranking(self):
        """Question 21: Comprehensive performance ranking system"""
        query = """
        SELECT 
            p.name as 'Player',
            p.country as 'Country',
            p.playing_role as 'Role',
            ROUND(
                -- Batting points calculation
                (p.total_runs * 0.01) + (p.batting_average * 0.5) + 
                (COALESCE(AVG(pp.strike_rate), 0) * 0.3) +
                -- Bowling points calculation
                (p.wickets_taken * 2) + 
                (CASE WHEN p.bowling_average > 0 THEN (50 - p.bowling_average) * 0.5 ELSE 0 END) +
                (CASE WHEN p.economy_rate > 0 THEN (6 - p.economy_rate) * 2 ELSE 0 END) +
                -- Fielding points calculation
                (p.catches * 3) + (p.stumpings * 5),
                2
            ) as 'Overall Performance Rating'
        FROM players p
        LEFT JOIN player_performances pp ON p.id = pp.player_id
        WHERE p.matches_played >= 5
        GROUP BY p.id, p.name, p.country, p.playing_role, p.total_runs, p.batting_average, 
                 p.wickets_taken, p.bowling_average, p.economy_rate, p.catches, p.stumpings
        ORDER BY 
            (p.total_runs * 0.01) + (p.batting_average * 0.5) + 
            (COALESCE(AVG(pp.strike_rate), 0) * 0.3) +
            (p.wickets_taken * 2) + 
            (CASE WHEN p.bowling_average > 0 THEN (50 - p.bowling_average) * 0.5 ELSE 0 END) +
            (CASE WHEN p.economy_rate > 0 THEN (6 - p.economy_rate) * 2 ELSE 0 END) +
            (p.catches * 3) + (p.stumpings * 5) DESC
        LIMIT 15
        """
        return self._execute_query(query, "Comprehensive Performance Ranking System")
    
    def query_22_head_to_head(self):
        """Question 22: Head-to-head team analysis"""
        query = """
        WITH team_matchups AS (
            SELECT 
                CASE 
                    WHEN team1 < team2 THEN team1 || ' vs ' || team2 
                    ELSE team2 || ' vs ' || team1 
                END as matchup,
                team1, team2, winning_team, victory_margin,
                match_date, venue_country, toss_decision
            FROM matches 
            WHERE match_date >= date('now', '-3 years')
            AND winning_team IS NOT NULL
        )
        SELECT 
            matchup as 'Team Matchup',
            COUNT(*) as 'Total Matches',
            SUM(CASE WHEN winning_team = SUBSTR(matchup, 1, INSTR(matchup, ' vs ') - 1) 
                THEN 1 ELSE 0 END) as 'Team 1 Wins',
            SUM(CASE WHEN winning_team = SUBSTR(matchup, INSTR(matchup, ' vs ') + 4) 
                THEN 1 ELSE 0 END) as 'Team 2 Wins',
            ROUND(AVG(victory_margin), 2) as 'Avg Victory Margin'
        FROM team_matchups
        GROUP BY matchup
        HAVING COUNT(*) >= 2
        ORDER BY COUNT(*) DESC
        """
        return self._execute_query(query, "Head-to-Head Team Analysis (Last 3 Years)")
    
    def query_23_recent_form(self):
        """Question 23: Recent player form analysis"""
        query = """
        WITH recent_performances AS (
            SELECT 
                p.name,
                pp.runs_scored,
                pp.strike_rate,
                m.match_date,
                ROW_NUMBER() OVER (PARTITION BY p.name ORDER BY m.match_date DESC) as match_rank
            FROM players p
            JOIN player_performances pp ON p.id = pp.player_id
            JOIN matches m ON pp.match_id = m.id
            WHERE m.match_date >= date('now', '-6 months')
            AND pp.runs_scored >= 0
        ),
        form_analysis AS (
            SELECT 
                name,
                AVG(CASE WHEN match_rank <= 3 THEN runs_scored END) as last_3_avg,
                AVG(CASE WHEN match_rank <= 5 THEN runs_scored END) as last_5_avg,
                SUM(CASE WHEN match_rank <= 5 AND runs_scored >= 50 THEN 1 ELSE 0 END) as fifties_plus,
                COUNT(CASE WHEN match_rank <= 5 THEN 1 END) as recent_matches
            FROM recent_performances
            GROUP BY name
            HAVING COUNT(CASE WHEN match_rank <= 5 THEN 1 END) >= 2
        )
        SELECT 
            name as 'Player',
            ROUND(last_3_avg, 2) as 'Last 3 Matches Avg',
            ROUND(last_5_avg, 2) as 'Last 5 Matches Avg',
            fifties_plus as '50+ Scores in Recent Matches',
            recent_matches as 'Recent Matches Played',
            CASE 
                WHEN last_3_avg >= 60 AND fifties_plus >= 2 THEN 'Excellent Form'
                WHEN last_3_avg >= 40 AND fifties_plus >= 1 THEN 'Good Form'
                WHEN last_3_avg >= 25 THEN 'Average Form'
                ELSE 'Below Average Form'
            END as 'Current Form Assessment'
        FROM form_analysis
        ORDER BY last_3_avg DESC
        """
        return self._execute_query(query, "Recent Player Form Analysis")
    
    def query_24_batting_partnerships(self):
        """Question 24: Successful batting partnerships"""
        query = """
        WITH partnerships AS (
            SELECT 
                p1.name as player1,
                p2.name as player2,
                pp1.runs_scored + pp2.runs_scored as partnership_runs,
                m.match_description,
                pp1.batting_position as pos1,
                pp2.batting_position as pos2
            FROM player_performances pp1
            JOIN player_performances pp2 ON pp1.match_id = pp2.match_id 
                AND ABS(pp2.batting_position - pp1.batting_position) = 1
            JOIN players p1 ON pp1.player_id = p1.id
            JOIN players p2 ON pp2.player_id = p2.id
            JOIN matches m ON pp1.match_id = m.id
            WHERE pp1.runs_scored > 0 AND pp2.runs_scored > 0
        )
        SELECT 
            CASE 
                WHEN player1 < player2 THEN player1 || ' & ' || player2 
                ELSE player2 || ' & ' || player1 
            END as 'Partnership',
            COUNT(*) as 'Total Partnerships',
            ROUND(AVG(partnership_runs), 2) as 'Average Partnership Runs',
            MAX(partnership_runs) as 'Highest Partnership',
            SUM(CASE WHEN partnership_runs >= 50 THEN 1 ELSE 0 END) as 'Partnerships 50+',
            ROUND(
                (SUM(CASE WHEN partnership_runs >= 50 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 
                2
            ) as 'Success Rate %'
        FROM partnerships
        GROUP BY 
            CASE 
                WHEN player1 < player2 THEN player1 || ' & ' || player2 
                ELSE player2 || ' & ' || player1 
            END
        HAVING COUNT(*) >= 2
        ORDER BY AVG(partnership_runs) DESC
        LIMIT 10
        """
        return self._execute_query(query, "Most Successful Batting Partnerships")
    
    def query_25_career_trajectory(self):
        """Question 25: Career trajectory analysis"""
        query = """
        WITH quarterly_stats AS (
            SELECT 
                p.name,
                strftime('%Y', m.match_date) || '-Q' || 
                ((CAST(strftime('%m', m.match_date) AS INTEGER) - 1) / 3 + 1) as quarter,
                AVG(pp.runs_scored) as avg_runs,
                AVG(pp.strike_rate) as avg_sr,
                COUNT(*) as matches_played,
                MIN(m.match_date) as quarter_start
            FROM players p
            JOIN player_performances pp ON p.id = pp.player_id
            JOIN matches m ON pp.match_id = m.id
            WHERE m.match_date >= date('now', '-2 years')
            AND pp.runs_scored >= 0
            GROUP BY p.name, 
                strftime('%Y', m.match_date) || '-Q' || 
                ((CAST(strftime('%m', m.match_date) AS INTEGER) - 1) / 3 + 1)
            HAVING COUNT(*) >= 1
        ),
        trajectory_analysis AS (
            SELECT 
                name,
                quarter,
                avg_runs,
                avg_sr,
                matches_played,
                quarter_start,
                LAG(avg_runs) OVER (PARTITION BY name ORDER BY quarter_start) as prev_avg
            FROM quarterly_stats
            ORDER BY name, quarter_start
        )
        SELECT 
            name as 'Player',
            COUNT(*) as 'Quarters with Data',
            ROUND(AVG(avg_runs), 2) as 'Overall Average',
            ROUND(
                AVG(CASE WHEN prev_avg IS NOT NULL AND prev_avg > 0
                    THEN ((avg_runs - prev_avg) / prev_avg * 100) END), 
                2
            ) as 'Avg Quarterly Change %',
            CASE 
                WHEN AVG(CASE WHEN prev_avg IS NOT NULL AND prev_avg > 0
                    THEN ((avg_runs - prev_avg) / prev_avg) END) > 0.1 THEN 'Career Ascending'
                WHEN AVG(CASE WHEN prev_avg IS NOT NULL AND prev_avg > 0
                    THEN ((avg_runs - prev_avg) / prev_avg) END) < -0.1 THEN 'Career Declining'
                ELSE 'Career Stable'
            END as 'Career Trajectory'
        FROM trajectory_analysis
        WHERE prev_avg IS NOT NULL
        GROUP BY name
        HAVING COUNT(*) >= 3
        ORDER BY AVG(CASE WHEN prev_avg IS NOT NULL AND prev_avg > 0
            THEN ((avg_runs - prev_avg) / prev_avg) END) DESC
        """
        return self._execute_query(query, "Career Trajectory Analysis")
    
    # Add these methods to your existing SQLQueries class in utils/sql_queries.py

    def get_queries_by_difficulty(self, difficulty):
        """Get queries filtered by difficulty level"""
        if difficulty == "Beginner":
            return {
                "Q1: All Players from India": self.query_1_indian_players,
                "Q2: Recent Matches (Last 30 Days)": self.query_2_recent_matches,
                "Q3: Top 10 Run Scorers": self.query_3_top_run_scorers,
                "Q4: Large Venues (50,000+ Capacity)": self.query_4_large_venues,
                "Q5: Team Win Statistics": self.query_5_team_wins,
                "Q6: Players by Role": self.query_6_players_by_role,
                "Q7: Highest Scores by Format": self.query_7_highest_scores_by_format,
                "Q8: Cricket Series Starting in 2024": self.query_8_series_2024
            }
        elif difficulty == "Intermediate":
            return {
                "Q9: Elite All-Rounders": self.query_9_allrounders,
                "Q10: Last 20 Completed Matches": self.query_10_completed_matches,
                "Q11: Multi-Format Player Performance": self.query_11_format_comparison,
                "Q12: Home vs Away Performance": self.query_12_home_away_analysis,
                "Q13: Century Partnerships": self.query_13_partnerships,
                "Q14: Most Economical Bowlers": self.query_14_venue_bowling,
                "Q19: Most Consistent Batsmen": self.query_19_consistent_batsmen,
                "Q20: Multi-Format Experience": self.query_20_format_experience
            }
        elif difficulty == "Advanced":
            return {
                "Q21: Performance Ranking System": self.query_21_performance_ranking,
                "Q22: Head-to-Head Team Analysis": self.query_22_head_to_head,
                "Q23: Recent Player Form Analysis": self.query_23_recent_form,
                "Q24: Successful Batting Partnerships": self.query_24_batting_partnerships,
                "Q25: Career Trajectory Analysis": self.query_25_career_trajectory
            }
        else:
            return self.get_all_queries()
    
    def get_all_queries(self):
        """Get all available queries"""
        all_queries = {}
        all_queries.update(self.get_queries_by_difficulty("Beginner"))
        all_queries.update(self.get_queries_by_difficulty("Intermediate"))
        all_queries.update(self.get_queries_by_difficulty("Advanced"))
        return all_queries
    
    def get_query_insights(self):
        """Get learning insights for each query"""
        return {
            "Q1: All Players from India": "Basic WHERE clause filtering - fundamental SQL concept for data selection.",
            "Q2: Recent Matches (Last 30 Days)": "Date filtering using datetime functions - important for time-based analysis.",
            "Q3: Top 10 Run Scorers": "ORDER BY with LIMIT - crucial for ranking and top-N queries.",
            "Q4: Large Venues (50,000+ Capacity)": "Numeric filtering with comparison operators - essential for statistical analysis.",
            "Q5: Team Win Statistics": "GROUP BY with COUNT - fundamental aggregation concept.",
            "Q6: Players by Role": "Data distribution analysis with GROUP BY and COUNT.",
            "Q7: Highest Scores by Format": "JOINs with GROUP BY and MAX - connecting related tables for analysis.",
            "Q8: Cricket Series Starting in 2024": "Date extraction functions with filtering - working with date components.",
            
            "Q9: Elite All-Rounders": "Multiple WHERE conditions - complex filtering criteria.",
            "Q10: Last 20 Completed Matches": "String concatenation with filtering and ordering.",
            "Q11: Multi-Format Player Performance": "CASE statements with JOINs - conditional logic in queries.",
            "Q12: Home vs Away Performance": "Complex CASE statements with conditional aggregation.",
            "Q13: Century Partnerships": "Self-joins for analyzing relationships between records.",
            "Q14: Most Economical Bowlers": "Advanced filtering with calculated fields and HAVING clause.",
            "Q19: Most Consistent Batsmen": "Statistical calculations using standard deviation - advanced math in SQL.",
            "Q20: Multi-Format Experience": "Multi-dimensional analysis across different categories.",
            
            "Q21: Performance Ranking System": "Complex scoring algorithm with multiple weighted factors.",
            "Q22: Head-to-Head Team Analysis": "Common Table Expressions (CTEs) with advanced string manipulation.",
            "Q23: Recent Player Form Analysis": "Window functions with ROW_NUMBER and complex conditional logic.",
            "Q24: Successful Batting Partnerships": "Advanced partnership analysis with success rate calculations.",
            "Q25: Career Trajectory Analysis": "LAG functions for trend analysis - expert-level time-series SQL."
        }
    
    def _execute_query(self, query, title):
        """Execute SQL query and return results with title"""
        try:
            df = self.db.execute_query(query)
            return df, title, query
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return pd.DataFrame(), title, query