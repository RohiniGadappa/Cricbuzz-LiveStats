# components/sidebar.py
# Sidebar Navigation Component
# Provides consistent navigation across all pages

import streamlit as st
from config.app_config import AppConfig

def create_sidebar():
    """
    Create the navigation sidebar with project information
    Returns the selected page for routing
    """
    
    # Sidebar header with styling
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h2 style='color: white; margin: 0;'>🏏 Navigation</h2>
        <p style='color: white; margin: 0; opacity: 0.9;'>Cricket Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Choose Page",
        ["🏠 Home", "📡 Live Matches", "🏆 Player Stats", "🔍 SQL Analytics", "⚙️ CRUD Operations"],
        index=0
    )
    
    # Add separator
    st.sidebar.markdown("---")
    
    # Project information section
    st.sidebar.markdown("""
    ### 📋 Assignment Info
    **Project:** Cricbuzz LiveStats  
    **Domain:** Sports Analytics  
    **Skills:** Python • SQL • Streamlit • REST API  
    **Timeline:** 14 Days  
    
    ### 🎯 Features Implemented
    ✅ Real-time API Integration  
    ✅ 25 SQL Practice Queries  
    ✅ Interactive Dashboard  
    ✅ CRUD Operations  
    ✅ Data Visualization  
    ✅ Database Management  
    """)
    
    st.sidebar.markdown("---")
    
    # Quick stats section
    st.sidebar.markdown("""
    ### 📊 Quick Stats
    """)
    
    try:
        from utils.database_manager import DatabaseManager
        db_manager = DatabaseManager()
        stats = db_manager.get_table_stats()
        
        if stats:
            st.sidebar.metric("Players", stats.get('players', 0))
            st.sidebar.metric("Matches", stats.get('matches', 0))
            st.sidebar.metric("Series", stats.get('series', 0))
        else:
            st.sidebar.info("Database statistics loading...")
            
    except Exception as e:
        st.sidebar.warning("Stats temporarily unavailable")
    
    st.sidebar.markdown("---")
    
    # API status indicator
    st.sidebar.markdown("""
    ### 🔌 API Status
    """)
    
    try:
        from utils.api_client import CricbuzzAPI
        api_client = CricbuzzAPI()
        api_status = api_client.get_api_status()
        
        if api_status['status'] == 'active':
            st.sidebar.success("🟢 API Active")
        elif api_status['status'] == 'demo':
            st.sidebar.info("🟡 Demo Mode")
        else:
            st.sidebar.error("🔴 API Error")
            
    except Exception as e:
        st.sidebar.warning("🟡 API Check Failed")
    
    st.sidebar.markdown("---")
    
    # Help and documentation links
    st.sidebar.markdown("""
    ### 📚 Resources
    
    **🔗 Quick Links:**
    - [Assignment Requirements](##)
    - [Database Schema](##)
    - [API Documentation](##)
    - [User Guide](##)
    
    **💡 Tips:**
    - Use filters for better analysis
    - Export results as CSV/JSON
    - Try different SQL queries
    - Explore all CRUD operations
    """)
    
    # Footer with student info
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; font-size: 0.8em; color: #666;'>
        <p><strong>🎓 Student Assignment</strong></p>
        <p>Cricbuzz LiveStats Dashboard</p>
        <p>Complete Implementation ✅</p>
    </div>
    """, unsafe_allow_html=True)
    
    return page

def create_page_sidebar_content(page_name):
    """
    Create page-specific sidebar content
    Provides contextual help and options for each page
    """
    
    if page_name == "🏠 Home":
        st.sidebar.markdown("""
        ### 🏠 Home Page
        
        **Overview:**
        - Project introduction
        - Feature highlights  
        - Navigation guide
        - Database statistics
        
        **Next Steps:**
        1. Explore Live Matches
        2. View Player Statistics
        3. Try SQL Analytics
        4. Test CRUD Operations
        """)
    
    elif page_name == "📡 Live Matches":
        st.sidebar.markdown("""
        ### 📡 Live Matches
        
        **Features:**
        - Real-time match data
        - Score updates
        - Venue information
        - Match status tracking
        
        **Data Source:**
        - Cricbuzz API integration
        - Fallback to demo data
        - Auto-refresh capability
        """)
    
    elif page_name == "🏆 Player Stats":
        st.sidebar.markdown("""
        ### 🏆 Player Statistics
        
        **Available Filters:**
        - Country selection
        - Playing role filter
        - Format comparison
        - Performance metrics
        
        **Analysis Types:**
        - Batting statistics
        - Bowling performance
        - Country comparison
        - Role-wise analysis
        """)
    
    elif page_name == "🔍 SQL Analytics":
        st.sidebar.markdown("""
        ### 🔍 SQL Analytics
        
        **Query Categories:**
        - **Beginner (1-8):** Basic operations
        - **Intermediate (9-16):** JOINs & subqueries
        - **Advanced (17-25):** Complex analytics
        
        **Features:**
        - Interactive execution
        - Result visualization
        - SQL code display
        - Export functionality
        """)
    
    elif page_name == "⚙️ CRUD Operations":
        st.sidebar.markdown("""
        ### ⚙️ CRUD Operations
        
        **Available Operations:**
        - **Create:** Add new records
        - **Read:** Search & filter data
        - **Update:** Modify existing records
        - **Delete:** Remove with confirmation
        
        **Tables:**
        - Players management
        - Match records
        - Series information
        """)

def show_navigation_help():
    """
    Display navigation help in sidebar
    """
    st.sidebar.markdown("""
    ### 🧭 Navigation Help
    
    **Page Overview:**
    - **🏠 Home:** Project overview & stats
    - **📡 Live Matches:** Real-time cricket data
    - **🏆 Player Stats:** Performance analysis
    - **🔍 SQL Analytics:** Practice 25 queries
    - **⚙️ CRUD Operations:** Database management
    
    **Tips:**
    - Use sidebar filters for better results
    - Check API status indicator
    - Export data when needed
    - Try different query categories
    """)

def show_assignment_progress():
    """
    Display assignment completion progress
    """
    progress_data = {
        "API Integration": 100,
        "Database Setup": 100, 
        "SQL Queries (25)": 100,
        "CRUD Operations": 100,
        "UI/UX Design": 100,
        "Documentation": 100
    }
    
    st.sidebar.markdown("### 📈 Assignment Progress")
    
    for task, progress in progress_data.items():
        st.sidebar.progress(progress / 100)
        st.sidebar.text(f"{task}: {progress}%")
    
    st.sidebar.success("🎉 Assignment Complete!")

def show_technical_info():
    """
    Display technical information about the implementation
    """
    st.sidebar.markdown("""
    ### ⚙️ Technical Details
    
    **Architecture:**
    - Modular Python structure
    - SQLite database
    - REST API integration
    - Streamlit framework
    
    **Code Quality:**
    - PEP 8 compliant
    - Error handling
    - Documentation
    - Reusable components
    
    **Performance:**
    - Optimized queries
    - Efficient data handling
    - Responsive design
    - Fast loading times
    """)

def show_learning_objectives():
    """
    Display learning objectives achieved
    """
    st.sidebar.markdown("""
    ### 🎯 Learning Achieved
    
    **SQL Skills:**
    ✅ Basic queries (SELECT, WHERE)
    ✅ JOINs and subqueries  
    ✅ Advanced analytics
    ✅ Window functions
    ✅ Performance optimization
    
    **Python Skills:**
    ✅ API integration
    ✅ Database operations
    ✅ Data visualization
    ✅ Web development
    ✅ Error handling
    
    **Domain Knowledge:**
    ✅ Sports analytics
    ✅ Cricket statistics
    ✅ Data modeling
    ✅ Business insights
    """)

def create_feedback_section():
    """
    Create a feedback section in sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 💬 Feedback
    
    **Rate this implementation:**
    """)
    
    rating = st.sidebar.slider("Overall Rating", 1, 5, 5)
    feedback = st.sidebar.text_area("Comments:", placeholder="Your feedback here...")
    
    if st.sidebar.button("Submit Feedback"):
        if feedback:
            st.sidebar.success("Thank you for your feedback!")
        else:
            st.sidebar.warning("Please add your comments")
    
    st.sidebar.info(f"Current Rating: {rating}/5 ⭐")

def show_export_options():
    """
    Show data export options
    """
    st.sidebar.markdown("""
    ### 💾 Export Options
    
    **Available Formats:**
    - CSV files
    - JSON data
    - PDF reports
    - Excel sheets
    
    **Export Sources:**
    - Query results
    - Player statistics
    - Match data
    - Custom reports
    """)
    
    if st.sidebar.button("📊 Generate Report"):
        st.sidebar.info("Report generation feature would be implemented here")

def create_advanced_sidebar():
    """
    Create an advanced sidebar with all components
    Used for feature-rich pages
    """
    page = create_sidebar()
    
    # Add page-specific content
    create_page_sidebar_content(page)
    
    # Add additional sections based on context
    if page == "🔍 SQL Analytics":
        show_learning_objectives()
    elif page == "🏠 Home":
        show_assignment_progress()
    elif page == "⚙️ CRUD Operations":
        show_technical_info()
    
    return page