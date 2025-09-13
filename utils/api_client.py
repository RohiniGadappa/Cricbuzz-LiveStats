import requests
import json
import time
from config.app_config import AppConfig

class CricbuzzAPIClient:
    """Client for interacting with Cricbuzz API"""
    
    def __init__(self):
        self.headers = AppConfig.get_api_headers()
        self.last_request_time = 0
        self.rate_limit_delay = 1  # 1 second between requests
        self.base_url = AppConfig.BASE_API_URL
    
    def _make_request(self, endpoint, params=None):
        """Make API request with rate limiting"""
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_request_time < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - (current_time - self.last_request_time))
        
        # Construct full URL
        url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            self.last_request_time = time.time()
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("Rate limit exceeded. Please wait...")
                time.sleep(60)  # Wait 1 minute
                return None
            else:
                print(f"API Error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("Request timeout")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON response")
            return None
    
    def get_api_status(self):
        """Check API status"""
        try:
            if AppConfig.is_demo_mode():
                return {'status': 'demo', 'message': 'Using demo data - no API key configured'}
            
            # Test with a simple endpoint
            response = self.get_live_matches()
            if response:
                return {'status': 'active', 'message': 'API is working'}
            else:
                return {'status': 'demo', 'message': 'API not responding, using demo data'}
        except:
            return {'status': 'error', 'message': 'API connection failed'}
    
    def get_recent_matches(self):
        """Get recent matches"""
        return self._make_request("/matches/v1/recent")
    
    def get_live_matches(self):
        """Get live matches"""
        return self._make_request("/matches/v1/live")
    
    def get_batting_rankings(self, format_type="odi"):
        """Get batting rankings"""
        return self._make_request("/stats/v1/rankings/batsmen", {"formatType": format_type})
    
    def get_bowling_rankings(self, format_type="odi"):
        """Get bowling rankings"""
        return self._make_request("/stats/v1/rankings/bowlers", {"formatType": format_type})
    
    def get_series_info(self):
        """Get series information"""
        return self._make_request("/series/v1/international")
    
    def get_match_details(self, match_id):
        """Get detailed match information"""
        return self._make_request(f"/mcenter/v1/{match_id}")
    
    def get_player_info(self, player_id):
        """Get player information"""
        return self._make_request(f"/stats/v1/player/{player_id}")
    
    # NEW METHODS FOR PLAYER STATS PAGE
    def get_player_rankings(self, format_type="test"):
        """Get player rankings - combines batting and bowling"""
        rankings_data = {}
        
        # Get batting rankings
        batting = self.get_batting_rankings(format_type)
        if batting:
            rankings_data['batting'] = batting
        
        # Get bowling rankings  
        bowling = self.get_bowling_rankings(format_type)
        if bowling:
            rankings_data['bowling'] = bowling
            
        return {'rank': rankings_data} if rankings_data else None
    
    def search_player(self, player_name):
        """Search for a player by name"""
        # Since there's no direct search endpoint, we'll use the rankings to find players
        formats = ['test', 'odi', 't20']
        
        for format_type in formats:
            # Search in batting rankings
            batting_data = self.get_batting_rankings(format_type)
            if batting_data:
                players = self._extract_players_from_rankings(batting_data, player_name)
                if players:
                    return players[0]  # Return first match
            
            # Search in bowling rankings
            bowling_data = self.get_bowling_rankings(format_type)
            if bowling_data:
                players = self._extract_players_from_rankings(bowling_data, player_name)
                if players:
                    return players[0]  # Return first match
        
        return None
    
    def _extract_players_from_rankings(self, rankings_data, search_name):
        """Extract players matching search name from rankings data"""
        found_players = []
        search_name_lower = search_name.lower()
        
        # This would need to be adapted based on your actual API response structure
        # For now, returning empty list as we'd need to see the actual response format
        return found_players
    
    def get_player_stats(self, player_id):
        """Get detailed player statistics"""
        return self.get_player_info(player_id)
    
    def get_team_players(self, team_name):
        """Get players from a team - extract from live matches"""
        matches = self.get_live_matches()
        team_players = []
        
        if matches and 'typeMatches' in matches:
            for match_type in matches['typeMatches']:
                if 'seriesMatches' in match_type:
                    for series in match_type['seriesMatches']:
                        if 'matches' in series.get('seriesAdWrapper', {}):
                            for match in series['seriesAdWrapper']['matches']:
                                match_info = match.get('matchInfo', {})
                                
                                # Check if team matches
                                team1 = match_info.get('team1', {}).get('teamName', '')
                                team2 = match_info.get('team2', {}).get('teamName', '')
                                
                                if team_name.lower() in team1.lower() or team_name.lower() in team2.lower():
                                    team_players.append({
                                        'team': team1 if team_name.lower() in team1.lower() else team2,
                                        'match': match_info.get('matchDescription', ''),
                                        'venue': match_info.get('venueInfo', {}).get('city', '')
                                    })
        
        return team_players

# Create a global instance
api_client = CricbuzzAPIClient()

# For backward compatibility, create an alias
CricbuzzAPI = CricbuzzAPIClient