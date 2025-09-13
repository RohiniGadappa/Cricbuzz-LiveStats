# utils/database_manager.py
# Database Manager Module
# Handles all database operations for Cricbuzz LiveStats

import sqlite3
import pandas as pd
import os
from datetime import datetime
from config.app_config import DatabaseConfig

class DatabaseManager:
    """
    Database Manager Class - Handles all database operations
    Following assignment requirements for SQL-based analytics
    """
    
    def __init__(self, db_path="data/cricbuzz_analytics.db"):
        """Initialize database connection with SQLite"""
        self.db_path = db_path
        self.ensure_data_directory()
        self.init_database()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def get_connection(self):
        """
        Get database connection - centralized as per assignment requirements
        Returns SQLite connection object
        """
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """
        Create database tables as per cricket data structure
        Implements complete schema for cricket analytics
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Players table - Core player information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                country TEXT,
                playing_role TEXT,
                batting_style TEXT,
                bowling_style TEXT,
                total_runs INTEGER DEFAULT 0,
                batting_average REAL DEFAULT 0.0,
                centuries INTEGER DEFAULT 0,
                wickets_taken INTEGER DEFAULT 0,
                bowling_average REAL DEFAULT 0.0,
                economy_rate REAL DEFAULT 0.0,
                catches INTEGER DEFAULT 0,
                stumpings INTEGER DEFAULT 0,
                matches_played INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Matches table - Match information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_description TEXT,
                team1 TEXT,
                team2 TEXT,
                venue_name TEXT,
                venue_city TEXT,
                venue_country TEXT,
                venue_capacity INTEGER,
                match_date DATE,
                match_format TEXT,
                winning_team TEXT,
                victory_margin INTEGER,
                victory_type TEXT,
                toss_winner TEXT,
                toss_decision TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Series table - Series information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                series_name TEXT,
                host_country TEXT,
                match_type TEXT,
                start_date DATE,
                total_matches INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Player performances table - Individual match performances
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_performances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                match_id INTEGER,
                runs_scored INTEGER DEFAULT 0,
                balls_faced INTEGER DEFAULT 0,
                strike_rate REAL DEFAULT 0.0,
                wickets_taken INTEGER DEFAULT 0,
                overs_bowled REAL DEFAULT 0.0,
                runs_conceded INTEGER DEFAULT 0,
                batting_position INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (match_id) REFERENCES matches(id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Insert sample data for demonstration
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """
        Insert sample cricket data for demonstration and SQL practice
        Loads realistic cricket data for testing all 25 SQL queries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM players")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample players data - Comprehensive cricket team data
        sample_players = [
            ("Virat Kohli", "India", "Batsman", "Right-handed", "Right-arm medium", 12000, 52.5, 43, 0, 0.0, 0.0, 89, 0, 245),
            ("Rohit Sharma", "India", "Batsman", "Right-handed", "Right-arm off-break", 9500, 48.2, 31, 8, 35.2, 5.8, 67, 0, 227),
            ("MS Dhoni", "India", "Wicket-keeper", "Right-handed", "Right-arm medium", 10773, 50.57, 10, 0, 0.0, 0.0, 123, 38, 350),
            ("Ravindra Jadeja", "India", "All-rounder", "Left-handed", "Left-arm orthodox", 2635, 35.26, 0, 213, 24.63, 2.39, 78, 0, 168),
            ("Jasprit Bumrah", "India", "Bowler", "Right-handed", "Right-arm fast", 85, 8.50, 0, 128, 20.94, 4.63, 12, 0, 64),
            ("Steve Smith", "Australia", "Batsman", "Right-handed", "Right-arm leg-break", 8010, 61.61, 27, 17, 54.7, 3.2, 106, 0, 131),
            ("Joe Root", "England", "Batsman", "Right-handed", "Right-arm off-break", 9500, 50.26, 24, 24, 45.8, 3.1, 89, 0, 189),
            ("Kane Williamson", "New Zealand", "Batsman", "Right-handed", "Right-arm off-break", 7115, 54.31, 22, 8, 52.2, 3.4, 78, 0, 131),
            ("Babar Azam", "Pakistan", "Batsman", "Right-handed", "Right-arm medium", 4442, 45.37, 13, 0, 0.0, 0.0, 56, 0, 98),
            ("Shaheen Afridi", "Pakistan", "Bowler", "Left-handed", "Left-arm fast", 123, 12.3, 0, 89, 23.98, 4.82, 15, 0, 36),
            ("David Warner", "Australia", "Batsman", "Left-handed", "Right-arm leg-break", 5455, 45.45, 18, 3, 42.0, 4.5, 78, 0, 120),
            ("Pat Cummins", "Australia", "Bowler", "Right-handed", "Right-arm fast", 945, 18.9, 0, 188, 28.94, 2.8, 45, 0, 67),
            ("Ben Stokes", "England", "All-rounder", "Left-handed", "Right-arm fast-medium", 4890, 36.0, 11, 99, 32.26, 3.2, 89, 0, 136),
            ("Trent Boult", "New Zealand", "Bowler", "Left-handed", "Left-arm fast-medium", 234, 13.6, 0, 317, 27.49, 4.85, 56, 0, 78),
            ("Quinton de Kock", "South Africa", "Wicket-keeper", "Left-handed", "Right-arm medium", 5440, 44.0, 15, 0, 0.0, 0.0, 134, 23, 124)
        ]
        
        cursor.executemany("""
            INSERT INTO players (name, country, playing_role, batting_style, bowling_style, 
                               total_runs, batting_average, centuries, wickets_taken, 
                               bowling_average, economy_rate, catches, stumpings, matches_played)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_players)
        
        # Sample matches data - Diverse match scenarios
        sample_matches = [
            ("India vs Australia, 1st ODI", "India", "Australia", "Wankhede Stadium", "Mumbai", "India", 33000, "2024-01-15", "ODI", "India", 36, "runs", "Australia", "bowl"),
            ("England vs New Zealand, T20I", "England", "New Zealand", "Lord's", "London", "England", 28000, "2024-02-20", "T20I", "New Zealand", 5, "wickets", "England", "bat"),
            ("Pakistan vs South Africa, Test", "Pakistan", "South Africa", "National Stadium", "Karachi", "Pakistan", 34000, "2024-03-10", "Test", "Pakistan", 7, "wickets", "Pakistan", "bat"),
            ("India vs England, 2nd ODI", "India", "England", "Eden Gardens", "Kolkata", "India", 66000, "2024-01-28", "ODI", "England", 8, "wickets", "India", "bat"),
            ("Australia vs West Indies, T20I", "Australia", "West Indies", "MCG", "Melbourne", "Australia", 100000, "2024-02-15", "T20I", "Australia", 42, "runs", "West Indies", "bowl"),
            ("India vs Pakistan, T20I", "India", "Pakistan", "Dubai International Stadium", "Dubai", "UAE", 25000, "2024-03-25", "T20I", "India", 6, "wickets", "Pakistan", "bat"),
            ("England vs Australia, Test", "England", "Australia", "The Oval", "London", "England", 27500, "2024-04-10", "Test", "Australia", 10, "wickets", "England", "bowl"),
            ("New Zealand vs South Africa, ODI", "New Zealand", "South Africa", "Eden Park", "Auckland", "New Zealand", 42000, "2024-04-20", "ODI", "New Zealand", 23, "runs", "South Africa", "bat")
        ]
        
        cursor.executemany("""
            INSERT INTO matches (match_description, team1, team2, venue_name, venue_city, 
                               venue_country, venue_capacity, match_date, match_format, 
                               winning_team, victory_margin, victory_type, toss_winner, toss_decision)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_matches)
        
        # Sample series data
        sample_series = [
            ("India vs Australia ODI Series 2024", "India", "ODI", "2024-01-15", 5),
            ("England vs New Zealand T20 Series", "England", "T20I", "2024-02-18", 3),
            ("Pakistan vs South Africa Test Series", "Pakistan", "Test", "2024-03-08", 2),
            ("ICC T20 World Cup 2024", "West Indies", "T20I", "2024-06-01", 55),
            ("Asia Cup 2024", "Pakistan", "ODI", "2024-08-15", 13)
        ]
        
        cursor.executemany("""
            INSERT INTO series (series_name, host_country, match_type, start_date, total_matches)
            VALUES (?, ?, ?, ?, ?)
        """, sample_series)
        
        # Sample player performances data for advanced queries
        sample_performances = [
            (1, 1, 85, 78, 108.97, 0, 0.0, 0, 1),  # Virat Kohli in match 1
            (2, 1, 124, 115, 107.83, 0, 0.0, 0, 2),  # Rohit Sharma in match 1
            (5, 1, 8, 15, 53.33, 3, 8.5, 45, 11),   # Bumrah bowling in match 1
            (1, 2, 45, 32, 140.63, 0, 0.0, 0, 3),   # Virat Kohli in match 2
            (7, 2, 67, 89, 75.28, 0, 0.0, 0, 4),    # Joe Root in match 2
            (13, 2, 23, 18, 127.78, 2, 3.2, 18, 6), # Ben Stokes all-round performance
            (6, 3, 178, 234, 76.07, 0, 0.0, 0, 1),  # Steve Smith in Test match
            (8, 4, 89, 98, 90.82, 0, 0.0, 0, 2),    # Kane Williamson
            (9, 5, 78, 67, 116.42, 0, 0.0, 0, 3),   # Babar Azam
            (10, 5, 12, 8, 150.0, 4, 4.0, 28, 9),   # Shaheen Afridi bowling
        ]
        
        cursor.executemany("""
            INSERT INTO player_performances (player_id, match_id, runs_scored, balls_faced, 
                                           strike_rate, wickets_taken, overs_bowled, runs_conceded, batting_position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_performances)
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=None):
        """
        Execute a SQL query and return results as DataFrame
        Used by SQL analytics module for all 25 queries
        """
        try:
            conn = self.get_connection()
            if params:
                df = pd.read_sql_query(query, conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Database query error: {e}")
            return pd.DataFrame()
    
    def insert_record(self, table, data):
        """
        Insert a new record into specified table
        Used by CRUD operations for Create functionality
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query, list(data.values()))
            record_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return record_id
        except Exception as e:
            print(f"Insert error: {e}")
            return None
    
    def update_record(self, table, record_id, data):
        """
        Update an existing record
        Used by CRUD operations for Update functionality
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
            
            cursor.execute(query, list(data.values()) + [record_id])
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected
        except Exception as e:
            print(f"Update error: {e}")
            return 0
    
    def delete_record(self, table, record_id):
        """
        Delete a record from specified table
        Used by CRUD operations for Delete functionality
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Delete related records first if necessary
            if table == "players":
                cursor.execute("DELETE FROM player_performances WHERE player_id = ?", (record_id,))
            elif table == "matches":
                cursor.execute("DELETE FROM player_performances WHERE match_id = ?", (record_id,))
            
            # Delete main record
            cursor.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected
        except Exception as e:
            print(f"Delete error: {e}")
            return 0
    
    def get_table_stats(self):
        """
        Get statistics about all tables
        Used for dashboard metrics
        """
        try:
            conn = self.get_connection()
            stats = {}
            
            tables = ["players", "matches", "series", "player_performances"]
            for table in tables:
                result = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn)
                stats[table] = result.iloc[0]['count']
            
            conn.close()
            return stats
        except Exception as e:
            print(f"Stats error: {e}")
            return {}
    
    def reset_database(self):
        """
        Reset database to initial state with sample data
        Used by CRUD operations for database reset functionality
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Drop all tables
            cursor.execute("DROP TABLE IF EXISTS player_performances")
            cursor.execute("DROP TABLE IF EXISTS matches")
            cursor.execute("DROP TABLE IF EXISTS series")
            cursor.execute("DROP TABLE IF EXISTS players")
            
            conn.commit()
            conn.close()
            
            # Reinitialize database
            self.init_database()
            return True
        except Exception as e:
            print(f"Reset error: {e}")
            return False