"""
Top Navigation Utility for VAYU AI
"""
import streamlit as st

def render_top_nav():
    """Renders a beige top navigation bar"""
    
    # CSS for top nav
    st.markdown("""
        <style>
        /* Hide sidebar */
        [data-testid="stSidebar"] {
            display: none;
        }
        
        /* Hide sidebar toggle */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        .st-emotion-cache-1h9usn1 {
            display: none;
        }
        
        /* Top nav container */
        .top-nav {
            background-color: #F5F5DC; /* Beige */
            padding: 10px 0;
            margin-bottom: 20px;
            border-radius: 5px;
            display: flex;
            justify-content: center;
            gap: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Nav links/buttons */
        .nav-link {
            text-decoration: none;
            color: #4B3621; /* Dark brown for contrast with beige */
            font-weight: 600;
            padding: 5px 15px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        
        .nav-link:hover {
            background-color: rgba(75, 54, 33, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Layout for nav buttons
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    
    with col1:
        st.markdown(f"<h3 style='color: #F5F5DC; margin: 0; padding-left: 10px;'>VAYU AI</h3>", unsafe_allow_html=True)
    
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    
    with col3:
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/1_📊_Dashboard.py")
            
    with col4:
        if st.button("🔗 Blockchain", use_container_width=True):
            st.switch_page("pages/2_🔗_Blockchain.py")
            
    # Inline style for the beige background behind buttons if needed, 
    # but Streamlit buttons have their own styling. 
    # We use a container-based approach with CSS for the "bar" look.
    st.markdown("""
        <div style="background-color: #F5F5DC; height: 3px; width: 100%; margin-top: -5px; border-radius: 2px;"></div>
    """, unsafe_allow_html=True)
