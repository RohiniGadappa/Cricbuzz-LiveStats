# config/app_config.py
# Application Configuration Module
# Centralized configuration management for Cricbuzz LiveStats

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AppConfig:
    """
    Application Configuration Class
    Centralizes all configuration settings for the application
    """
    
    # Application Settings
    APP_TITLE = "🏏 Cricbuzz LiveStats"
    APP_ICON = "🏏"
    APP_DESCRIPTION = "Real-Time Cricket Insights & SQL-Based Analytics"
    
    # API Configuration
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "demo_key")
    RAPIDAPI_HOST = "cricbuzz-cricket2.p.rapidapi.com"
    BASE_API_URL = "https://cricbuzz-cricket2.p.rapidapi.com"
    
    # Database Configuration
    DATABASE_PATH = "data/cricbuzz_analytics.db"
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    
    # UI Configuration
    SIDEBAR_WIDTH = 300
    CHART_HEIGHT = 400
    TABLE_HEIGHT = 600
    
    # Colors and Styling
    PRIMARY_COLOR = "#FF6B35"
    SECONDARY_COLOR = "#F7931E"
    ACCENT_COLOR = "#1f77b4"
    BACKGROUND_GRADIENT = "linear-gradient(90deg, #FF6B35, #F7931E)"
    
    # Query Categories
    BEGINNER_QUERIES = list(range(1, 9))    # Questions 1-8
    INTERMEDIATE_QUERIES = list(range(9, 17))  # Questions 9-16
    ADVANCED_QUERIES = list(range(17, 26))    # Questions 17-25
    
    @classmethod
    def get_api_headers(cls):
        """Get API headers for Cricbuzz requests"""
        return {
            "X-RapidAPI-Key": cls.RAPIDAPI_KEY,
            "X-RapidAPI-Host": cls.RAPIDAPI_HOST
        }
    
    @classmethod
    def is_demo_mode(cls):
        """Check if running in demo mode (without valid API key)"""
        return cls.RAPIDAPI_KEY == "demo_key" or not cls.RAPIDAPI_KEY

class DatabaseConfig:
    """
    Database Configuration Class
    Settings specific to database operations
    """
    
    # Connection settings
    CONNECTION_TIMEOUT = 30
    MAX_CONNECTIONS = 10
    
    # Table names
    PLAYERS_TABLE = "players"
    MATCHES_TABLE = "matches"
    SERIES_TABLE = "series"
    PERFORMANCES_TABLE = "player_performances"
    
    # Query limits
    DEFAULT_LIMIT = 100
    MAX_LIMIT = 1000
    
    # Sample data settings
    LOAD_SAMPLE_DATA = True
    SAMPLE_PLAYERS_COUNT = 10
    SAMPLE_MATCHES_COUNT = 5