import streamlit as st
import plotly.express as exp
import app.data.incidents as CyberFuncs

def debug(*args):
    """
    Debugging function to print arguments to console.
    """
    for arg in args:
        print("DEBUG: {}".format(arg)) 

def check_login():
    """
    Check if user is logged in and handle redirection.
    """
    # 1. Initialize Default State
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # 2. The Check
    if not st.session_state.logged_in:
        st.warning("Please log in to access the IT Tickets dashboard.")
        
        # 3. Navigation Button
        if st.button("Go to Login Page"):
            st.switch_page("Home.py") 
            
        st.stop()

def barchart(data, xAxis: str):
    """
    Create and display a bar chart using Plotly Express.
    """
    fig = exp.bar(data, x=xAxis, title="Cyber Incidents by {}".format(xAxis.capitalize()))
    st.plotly_chart(fig)

def apply_filter(selected_category: str):
    """
    Create a filter query based on the selected category.
    """
    filter_query = f"category = '{selected_category}'"
    return filter_query

def RowColumnCnt(column: str):
    """
    Displays number of rows in the bar chart filtered output
    """
    rowCnt = CyberFuncs.TotalIncidents(filterquery, column)
    st.text("Row Count: {}".format(rowCnt))

def filterquery():
    """
    Create a filter query based on user selections.
    """
    st.divider()
    categories = CyberFuncs.get_incident_categories()
    selected_category = st.selectbox("Select Incident Category", categories)
    filter_query = f"category = '{selected_category}'"
    return filter_query

def createincident():
    """
    Create a new cyber incident entry.
    """
    st.subheader("Create New Cyber Incident")
    title = st.text_input("Incident Title")
    category = st.selectbox("Category", CyberFuncs.get_incident_categories())
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Description")

    if st.button("Submit Incident"):
        if title and description:
            CyberFuncs.insert_incident(title, category, severity, description)
            st.success("Incident created successfully!")
        else:
            st.error("Please fill in all required fields.")

if __name__ == "__main__":
    check_login()
    
    st.title("Cyber Analytics Dashboard")
    
    # Filter and display bar chart
    filterquery = filterquery()
    data = CyberFuncs.get_filtered_incidents(filterquery)
    
    if not data.empty:
        selected_column = st.selectbox("Select Column for Bar Chart", ["category", "severity"])
        RowColumnCnt(selected_column)
        barchart(data, selected_column)
    else:
        st.info("No incidents found for the selected filter.")
    
    # Create new incident
    createincident()   