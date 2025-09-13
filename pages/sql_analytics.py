# pages/sql_analytics.py
# SQL Analytics Page Implementation
# Interactive execution of all 25 SQL practice queries

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from components.styles import create_main_header, create_stat_card
from components.sidebar import create_page_sidebar_content
from utils.database_manager import DatabaseManager
from utils.sql_queries import SQLQueries
from config.app_config import AppConfig

def sql_analytics_page():
    """
    SQL Analytics Page - 25 SQL queries implementation
    Assignment Requirement: Integrates 25+ advanced SQL queries with tabular outputs
    """
    create_main_header()
    st.header("🔍 SQL Analytics & Practice Queries")
    
    # Add page-specific sidebar content
    create_page_sidebar_content("🔍 SQL Analytics")
    
    st.markdown("""
    This section implements all **25 SQL practice questions** from the assignment, organized by difficulty level.  
    Each query demonstrates different SQL concepts and provides real-world cricket analytics insights.
    """)
    
    # Initialize SQL queries class
    db_manager = DatabaseManager()
    sql_queries = SQLQueries(db_manager)
    
    # Sidebar for query selection
    st.sidebar.header("📝 Query Selection")
    
    difficulty_level = st.sidebar.selectbox(
        "Select Difficulty Level",
        ["Beginner (1-8)", "Intermediate (9-16)", "Advanced (17-25)", "All Queries"]
    )
    
    # Get queries based on difficulty
    if difficulty_level == "Beginner (1-8)":
        available_queries = sql_queries.get_queries_by_difficulty("Beginner")
    elif difficulty_level == "Intermediate (9-16)":
        available_queries = sql_queries.get_queries_by_difficulty("Intermediate")
    elif difficulty_level == "Advanced (17-25)":
        available_queries = sql_queries.get_queries_by_difficulty("Advanced")
    else:  # All Queries
        available_queries = sql_queries.get_all_queries()
    
    selected_query = st.sidebar.selectbox(
        "Choose Query",
        list(available_queries.keys())
    )
    
    # Query execution controls
    st.sidebar.markdown("---")
    execute_button = st.sidebar.button("🚀 Execute Query", type="primary")
    
    if st.sidebar.button("📊 Show Query Categories"):
        st.session_state['show_categories'] = True
    
    if st.sidebar.button("💡 Learning Guide"):
        st.session_state['show_learning_guide'] = True
    
    # Main content area
    if execute_button:
        execute_selected_query(sql_queries, available_queries, selected_query)
    
    # Show categories if requested
    if hasattr(st.session_state, 'show_categories') and st.session_state.show_categories:
        show_query_categories()
        st.session_state.show_categories = False
    
    # Show learning guide if requested  
    if hasattr(st.session_state, 'show_learning_guide') and st.session_state.show_learning_guide:
        show_learning_guide()
        st.session_state.show_learning_guide = False
    
    # Default content when no query is executed
    if not execute_button:
        show_default_content()

def execute_selected_query(sql_queries, available_queries, selected_query):
    """Execute the selected SQL query and display results"""
    query_func = available_queries[selected_query]
    
    with st.spinner(f"Executing {selected_query}..."):
        try:
            df_result, query_title, sql_code = query_func()
            
            # Display query information
            st.subheader(f"📊 {query_title}")
            
            # Show SQL code in expandable section
            with st.expander("👨‍💻 View SQL Code", expanded=False):
                st.code(sql_code, language='sql')
            
            # Display results
            if not df_result.empty:
                st.success(f"✅ Query executed successfully! Found {len(df_result)} records.")
                
                # Display data table with styling
                st.markdown("### 📋 Query Results")
                st.dataframe(df_result, use_container_width=True)
                
                # Add visualization if appropriate
                if len(df_result.columns) >= 2 and len(df_result) > 1:
                    create_query_visualization(df_result, query_title)
                
                # Export functionality
                create_export_options(df_result, query_title)
                
                # Query insights
                show_query_insights(selected_query, df_result)
                
            else:
                st.warning("⚠️ No results found for this query.")
                st.info("This might be due to:")
                st.markdown("""
                - No data matching the query criteria
                - Database constraints or filters
                - Sample data limitations
                """)
            
        except Exception as e:
            st.error(f"❌ Error executing query: {str(e)}")
            st.error("Please check the database connection and query syntax.")
            
            with st.expander("🔧 Debugging Information"):
                st.write("**Error Details:**")
                st.exception(e)

def create_query_visualization(df_result, query_title):
    """Create appropriate visualization based on query results"""
    st.markdown("### 📈 Data Visualization")
    
    # Chart type selection
    col1, col2 = st.columns([1, 3])
    
    with col1:
        chart_type = st.selectbox(
            "Chart Type", 
            ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Heatmap"]
        )
    
    with col2:
        # Get numeric columns for visualization
        numeric_cols = df_result.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 1:
            y_axis = st.selectbox("Y-Axis (Numeric)", numeric_cols)
            x_axis = st.selectbox("X-Axis", df_result.columns.tolist())
        else:
            st.warning("No numeric columns available for visualization")
            return
    
    # Create visualization based on selection
    try:
        if chart_type == "Bar Chart":
            fig = px.bar(
                df_result.head(15), 
                x=x_axis, 
                y=y_axis,
                title=f"{query_title} - Bar Chart",
                color=y_axis,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(xaxis_tickangle=-45)
            
        elif chart_type == "Line Chart":
            fig = px.line(
                df_result.head(15), 
                x=x_axis, 
                y=y_axis,
                title=f"{query_title} - Line Chart",
                markers=True
            )
            
        elif chart_type == "Pie Chart" and len(df_result) <= 12:
            fig = px.pie(
                df_result.head(8), 
                values=y_axis, 
                names=x_axis,
                title=f"{query_title} - Pie Chart"
            )
            
        elif chart_type == "Scatter Plot" and len(numeric_cols) >= 2:
            color_col = numeric_cols[1] if len(numeric_cols) > 2 else None
            fig = px.scatter(
                df_result, 
                x=numeric_cols[0], 
                y=numeric_cols[1],
                color=color_col,
                title=f"{query_title} - Scatter Plot",
                hover_data=df_result.columns[:3].tolist()
            )
            
        elif chart_type == "Heatmap" and len(numeric_cols) >= 2:
            # Create correlation heatmap for numeric columns
            corr_data = df_result[numeric_cols].corr()
            fig = px.imshow(
                corr_data,
                title=f"{query_title} - Correlation Heatmap",
                color_continuous_scale='RdBu'
            )
            
        else:
            # Default to bar chart
            fig = px.bar(
                df_result.head(10), 
                x=x_axis, 
                y=y_axis,
                title=f"{query_title} - Data Visualization"
            )
        
        # Update layout for better appearance
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as viz_error:
        st.warning(f"Visualization error: {viz_error}")
        st.info("Try selecting different columns or chart types for better visualization.")

def create_export_options(df_result, query_title):
    """Create export functionality for query results"""
    st.markdown("### 💾 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV download
        csv = df_result.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"{query_title.replace(' ', '_')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # JSON download
        json_str = df_result.to_json(orient='records', indent=2)
        st.download_button(
            label="📋 Download JSON",
            data=json_str,
            file_name=f"{query_title.replace(' ', '_')}.json",
            mime="application/json"
        )
    
    with col3:
        # Excel download (requires openpyxl)
        try:
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_result.to_excel(writer, index=False, sheet_name='Query_Results')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name=f"{query_title.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except ImportError:
            st.info("Excel export requires openpyxl package")

def show_query_insights(selected_query, df_result):
    """Show insights and learning points for the executed query"""
    st.markdown("### 💡 Query Insights")
    
    # Get insights from SQL queries class
    sql_queries_class = SQLQueries(DatabaseManager())
    insights = sql_queries_class.get_query_insights()
    
    insight = insights.get(selected_query, "This query demonstrates advanced SQL techniques for cricket analytics.")
    
    st.info(insight)
    
    # Additional statistical insights if applicable
    if not df_result.empty and len(df_result) > 1:
        st.markdown("#### 📊 Result Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(df_result))
        
        with col2:
            numeric_cols = df_result.select_dtypes(include=[np.number]).columns
            st.metric("Numeric Columns", len(numeric_cols))
        
        with col3:
            st.metric("Data Columns", len(df_result.columns))
        
        # Show data types and basic statistics
        if len(numeric_cols) > 0:
            with st.expander("📈 Statistical Summary"):
                st.dataframe(df_result[numeric_cols].describe())

def show_query_categories():
    """Display overview of all query categories"""
    st.header("📋 SQL Query Categories Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_stat_card("""
        <h3>🟢 Beginner (Questions 1-8)</h3>
        <h4>Core SQL Fundamentals</h4>
        <ul>
        <li>Basic SELECT statements</li>
        <li>WHERE clause filtering</li>
        <li>ORDER BY and GROUP BY</li>
        <li>Simple aggregate functions</li>
        <li>Date/time operations</li>
        <li>String manipulations</li>
        <li>DISTINCT operations</li>
        <li>Basic table joins</li>
        </ul>
        <p><em>Perfect for SQL beginners and foundational concepts</em></p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_stat_card("""
        <h3>🟡 Intermediate (Questions 9-16)</h3>
        <h4>Advanced Query Techniques</h4>
        <ul>
        <li>Complex JOINs (INNER, LEFT, RIGHT)</li>
        <li>Subqueries and correlated queries</li>
        <li>CASE statements</li>
        <li>Advanced GROUP BY with HAVING</li>
        <li>Multiple table analysis</li>
        <li>Conditional aggregations</li>
        <li>Data transformation</li>
        <li>Performance analysis queries</li>
        </ul>
        <p><em>Builds on fundamentals with real-world complexity</em></p>
        """), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_stat_card("""
        <h3>🔴 Advanced (Questions 17-25)</h3>
        <h4>Expert-Level Analytics</h4>
        <ul>
        <li>Window functions (ROW_NUMBER, RANK)</li>
        <li>Common Table Expressions (CTEs)</li>
        <li>Statistical calculations</li>
        <li>Time-series analysis</li>
        <li>LAG/LEAD functions</li>
        <li>Complex business logic</li>
        <li>Performance ranking systems</li>
        <li>Predictive analytics queries</li>
        </ul>
        <p><em>Professional-level SQL for data analysis</em></p>
        """), unsafe_allow_html=True)

def show_learning_guide():
    """Display SQL learning guide and best practices"""
    st.header("🎓 SQL Learning Guide")
    
    # Learning path
    st.subheader("📚 Recommended Learning Path")
    
    learning_tabs = st.tabs(["🌱 Getting Started", "📈 Building Skills", "🚀 Mastery", "💼 Best Practices"])
    
    with learning_tabs[0]:
        st.markdown("""
        ### 🌱 Getting Started with SQL
        
        **Step 1: Understand the Database Schema**
        ```sql
        -- Explore tables and their structure
        SELECT name FROM sqlite_master WHERE type='table';
        
        -- Check table columns
        PRAGMA table_info(players);
        ```
        
        **Step 2: Basic SELECT Queries**
        ```sql
        -- Simple data retrieval
        SELECT name, country FROM players LIMIT 5;
        
        -- Filtering data
        SELECT * FROM players WHERE country = 'India';
        ```
        
        **Step 3: Sorting and Grouping**
        ```sql
        -- Sort results
        SELECT name, total_runs FROM players ORDER BY total_runs DESC;
        
        -- Group and aggregate
        SELECT country, COUNT(*) FROM players GROUP BY country;
        ```
        
        **🎯 Practice Queries:** Start with Questions 1-4 for basic concepts.
        """)
    
    with learning_tabs[1]:
        st.markdown("""
        ### 📈 Building Advanced Skills
        
        **JOINs - Connecting Related Data**
        ```sql
        -- INNER JOIN example
        SELECT p.name, m.match_description 
        FROM players p 
        INNER JOIN player_performances pp ON p.id = pp.player_id
        INNER JOIN matches m ON pp.match_id = m.id;
        ```
        
        **Subqueries - Queries within Queries**
        ```sql
        -- Find players with above-average runs
        SELECT name, total_runs 
        FROM players 
        WHERE total_runs > (SELECT AVG(total_runs) FROM players);
        ```
        
        **CASE Statements - Conditional Logic**
        ```sql
        -- Categorize players by performance
        SELECT name,
            CASE 
                WHEN batting_average >= 50 THEN 'Excellent'
                WHEN batting_average >= 35 THEN 'Good'
                ELSE 'Average'
            END as performance_category
        FROM players;
        ```
        
        **🎯 Practice Queries:** Work through Questions 9-12 for JOIN mastery.
        """)
    
    with learning_tabs[2]:
        st.markdown("""
        ### 🚀 Advanced Mastery
        
        **Window Functions - Advanced Analytics**
        ```sql
        -- Rank players by runs with ties
        SELECT name, total_runs,
            RANK() OVER (ORDER BY total_runs DESC) as rank
        FROM players;
        
        -- Running totals and moving averages
        SELECT name, total_runs,
            SUM(total_runs) OVER (ORDER BY total_runs) as running_total
        FROM players;
        ```
        
        **Common Table Expressions (CTEs)**
        ```sql
        -- Complex multi-step analysis
        WITH top_batsmen AS (
            SELECT name, total_runs, batting_average
            FROM players 
            WHERE total_runs > 5000
        )
        SELECT * FROM top_batsmen 
        WHERE batting_average > 40;
        ```
        
        **Statistical Analysis**
        ```sql
        -- Calculate standard deviation for consistency
        SELECT name,
            SQRT(AVG(runs_scored * runs_scored) - AVG(runs_scored) * AVG(runs_scored)) as consistency
        FROM player_performances pp
        JOIN players p ON pp.player_id = p.id
        GROUP BY name;
        ```
        
        **🎯 Practice Queries:** Master Questions 17-25 for expert-level skills.
        """)
    
    with learning_tabs[3]:
        st.markdown("""
        ### 💼 SQL Best Practices
        
        **Performance Optimization**
        - Use indexes on frequently queried columns
        - Limit results with LIMIT clause when appropriate
        - Use EXISTS instead of IN for better performance
        - Avoid SELECT * in production queries
        
        **Code Quality**
        ```sql
        -- Good: Clear, readable formatting
        SELECT 
            p.name,
            p.country,
            COUNT(pp.id) as matches_played,
            AVG(pp.runs_scored) as avg_runs
        FROM players p
        LEFT JOIN player_performances pp ON p.id = pp.player_id
        WHERE p.country IN ('India', 'Australia')
        GROUP BY p.name, p.country
        HAVING COUNT(pp.id) >= 5
        ORDER BY avg_runs DESC;
        ```
        
        **Error Handling**
        - Always check for NULL values with appropriate handling
        - Use COALESCE or CASE for NULL replacements
        - Validate data types in calculations
        - Include meaningful aliases for readability
        
        **Documentation**
        - Comment complex queries
        - Use meaningful table and column aliases
        - Document business logic in query comments
        - Maintain consistent formatting style
        """)

def show_default_content():
    """Show default content when no query is selected"""
    st.subheader("📋 SQL Query Practice Overview")
    
    st.markdown("""
    Welcome to the SQL Analytics section! This implements all **25 practice questions** from the assignment.
    
    ### 🎯 Learning Objectives
    - Master different SQL concepts from basic to advanced
    - Practice with real cricket data scenarios
    - Understand database analytics in sports domain
    - Learn query optimization and complex joins
    
    ### 📊 How to Use This Section
    1. **Select Difficulty Level** from the sidebar (Beginner, Intermediate, or Advanced)
    2. **Choose a Query** from the dropdown list
    3. **Click 'Execute Query'** to run the SQL statement
    4. **View Results** in the data table below
    5. **Explore Visualizations** for better insights
    6. **Check SQL Code** to understand the implementation
    7. **Download Results** in CSV, JSON, or Excel format
    """)
    
    # Quick stats about available queries
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Queries", "25", "Complete set")
    
    with col2:
        st.metric("Beginner Level", "8", "Questions 1-8")
    
    with col3:
        st.metric("Intermediate", "8", "Questions 9-16")
    
    with col4:
        st.metric("Advanced", "9", "Questions 17-25")
    
    st.markdown("---")
    
    # Sample queries showcase
    st.subheader("🔥 Featured Queries")
    
    featured_cols = st.columns(3)
    
    with featured_cols[0]:
        st.markdown(create_stat_card("""
        <h4>🟢 Beginner Highlight</h4>
        <h5>Q3: Top 10 Run Scorers</h5>
        <p>Perfect introduction to ORDER BY and LIMIT clauses. Learn basic ranking and data limitation techniques.</p>
        <code>ORDER BY total_runs DESC LIMIT 10</code>
        """), unsafe_allow_html=True)
    
    with featured_cols[1]:
        st.markdown(create_stat_card("""
        <h4>🟡 Intermediate Highlight</h4>
        <h5>Q11: Multi-Format Performance</h5>
        <p>Master CASE statements with JOINs for cross-format analysis. Essential for sports analytics.</p>
        <code>CASE WHEN match_format = 'Test'...</code>
        """), unsafe_allow_html=True)
    
    with featured_cols[2]:
        st.markdown(create_stat_card("""
        <h4>🔴 Advanced Highlight</h4>
        <h5>Q25: Career Trajectory Analysis</h5>
        <p>Expert-level time-series analysis with LAG functions and trend calculations. Professional analytics.</p>
        <code>LAG(avg_runs) OVER (ORDER BY...)</code>
        """), unsafe_allow_html=True)
    
    # Database schema quick reference
    st.markdown("---")
    st.subheader("🗄️ Database Schema Quick Reference")
    
    schema_tabs = st.tabs(["Players", "Matches", "Performances", "Series"])
    
    with schema_tabs[0]:
        st.markdown("""
        **Players Table Structure:**
        ```sql
        CREATE TABLE players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT,
            playing_role TEXT,
            batting_style TEXT,
            bowling_style TEXT,
            total_runs INTEGER,
            batting_average REAL,
            centuries INTEGER,
            wickets_taken INTEGER,
            bowling_average REAL,
            economy_rate REAL,
            catches INTEGER,
            stumpings INTEGER,
            matches_played INTEGER
        );
        ```
        """)
    
    with schema_tabs[1]:
        st.markdown("""
        **Matches Table Structure:**
        ```sql
        CREATE TABLE matches (
            id INTEGER PRIMARY KEY,
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
            toss_decision TEXT
        );
        ```
        """)
    
    with schema_tabs[2]:
        st.markdown("""
        **Player Performances Table:**
        ```sql
        CREATE TABLE player_performances (
            id INTEGER PRIMARY KEY,
            player_id INTEGER,
            match_id INTEGER,
            runs_scored INTEGER,
            balls_faced INTEGER,
            strike_rate REAL,
            wickets_taken INTEGER,
            overs_bowled REAL,
            runs_conceded INTEGER,
            batting_position INTEGER,
            FOREIGN KEY (player_id) REFERENCES players(id),
            FOREIGN KEY (match_id) REFERENCES matches(id)
        );
        ```
        """)
    
    with schema_tabs[3]:
        st.markdown("""
        **Series Table Structure:**
        ```sql
        CREATE TABLE series (
            id INTEGER PRIMARY KEY,
            series_name TEXT,
            host_country TEXT,
            match_type TEXT,
            start_date DATE,
            total_matches INTEGER
        );
        ```
        """)
    
    # Quick database statistics
    try:
        db_manager = DatabaseManager()
        stats = db_manager.get_table_stats()
        
        if stats:
            st.markdown("### 📈 Current Database Statistics")
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.metric("Players", stats.get('players', 0))
            with metric_cols[1]:
                st.metric("Matches", stats.get('matches', 0))
            with metric_cols[2]:
                st.metric("Performances", stats.get('player_performances', 0))
            with metric_cols[3]:
                st.metric("Series", stats.get('series', 0))
                
    except Exception as e:
        st.info("Database statistics will be available once the database is initialized.")

# Additional utility functions for the SQL Analytics page
def format_sql_code(sql_code):
    """Format SQL code for better display"""
    # Basic SQL formatting (could be enhanced with sqlparse library)
    formatted = sql_code.replace(',', ',\n    ')
    formatted = formatted.replace('FROM', '\nFROM')
    formatted = formatted.replace('WHERE', '\nWHERE')
    formatted = formatted.replace('GROUP BY', '\nGROUP BY')
    formatted = formatted.replace('ORDER BY', '\nORDER BY')
    formatted = formatted.replace('HAVING', '\nHAVING')
    return formatted

def get_query_complexity_score(sql_code):
    """Calculate complexity score for SQL query"""
    score = 0
    
    # Count different SQL elements
    joins = sql_code.upper().count('JOIN')
    subqueries = sql_code.upper().count('SELECT') - 1  # Subtract main SELECT
    case_statements = sql_code.upper().count('CASE')
    window_functions = sql_code.upper().count('OVER')
    ctes = sql_code.upper().count('WITH')
    
    # Calculate score
    score += joins * 2
    score += subqueries * 3
    score += case_statements * 2
    score += window_functions * 4
    score += ctes * 3
    
    return score

def show_execution_plan(query):
    """Show query execution plan for learning purposes"""
    try:
        db_manager = DatabaseManager()
        plan_query = f"EXPLAIN QUERY PLAN {query}"
        plan_result = db_manager.execute_query(plan_query)
        
        if not plan_result.empty:
            st.subheader("🔧 Query Execution Plan")
            st.dataframe(plan_result, use_container_width=True)
            st.info("The execution plan shows how SQLite processes your query.")
    except Exception as e:
        st.warning(f"Could not generate execution plan: {e}")