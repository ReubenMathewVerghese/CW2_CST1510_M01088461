import streamlit as st
import app.data.tickets as tickets
import plotly.express as exp
from openai import OpenAI


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

def selectcol():
    """
    create a selectbox for ticket categories
    return selected category
    """
    st.divider()
    categories = tickets.get_ticket_categories()
    selected_category = st.selectbox("Select Ticket Category", categories)
    return selected_category

def RowColumnCnt(column: str):
    """
    Displays number of rows in the bar chart filtered output
    """
    rowCnt = tickets.TotalTickets(filterquery, column)
    st.text("Row Count: {}".format(rowCnt))

def barchart(data, xAxis: str):
    """
    Create and display a bar chart using Plotly Express.
    """
    fig = exp.bar(data, x=xAxis, title="IT Tickets by {}".format(xAxis.capitalize()))
    st.plotly_chart(fig)

def filterquery():
    """
    Create a filter query based on user selections.
    """
    st.divider()
    st.subheader("Filter Tickets")
    
    # Date Range Filter
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    # Status Filter
    status_options = tickets.get_ticket_statuses()
    selected_status = st.multiselect("Select Status", status_options, default=status_options)
    
    # Priority Filter
    priority_options = tickets.get_ticket_priorities()
    selected_priority = st.multiselect("Select Priority", priority_options, default=priority_options)
    
    # Build filter query
    query_parts = []
    if start_date:
        query_parts.append(f"created_date >= '{start_date}'")
    if end_date:
        query_parts.append(f"created_date <= '{end_date}'")
    if selected_status:
        status_list = "', '".join(selected_status)
        query_parts.append(f"status IN ('{status_list}')")
    if selected_priority:
        priority_list = "', '".join(selected_priority)
        query_parts.append(f"priority IN ('{priority_list}')")
    
    filter_query = " AND ".join(query_parts) if query_parts else "1=1"
    return filter_query

def Filters() -> None:
    """
    Creates widgets for filters which include textboxes, checkboxes, and date inputs
    When apply filters button clicked, pass user input values to FilterQuery()
    """
    with st.sidebar:
        st.title("Filters")
        
        with st.expander("**ID**"):
            idStart = str(st.text_input("Start Value"))
            idStop = str(st.text_input("Stop Value"))
            
        with st.expander("**Subject**"):
            # Returns a list, so we cast to tuple for FilterQuery
            titleFil = tuple(st.multiselect("Subject", ("Printer not working", "Password reset request", "VPN connection issue", "Network outage", "Access request", "Software installation needed", "Malware alert", "Laptop not booting", "System Crash", "Email not syncing")))

        with st.expander("**Priority**"):
            prioFil = tuple(st.multiselect("Priority", ("low", "medium", "high", "urgent")))
            
        with st.expander("**Status**"):
            statusFil = tuple(st.multiselect("Status", ("open", "in progress", "resolved")))
        
        with st.expander("**Date**"):
            # Note: date_input returns a datetime.date object
            dateStart = st.date_input("Start Value", value=None)
            dateStop = st.date_input("Stop Value", value=None)
            
        if st.button("Apply Filters"):
            filterquery(idStart, idStop, titleFil, prioFil, statusFil, str(dateStart), str(dateStop))
            global filterapply
            filterapply = True
  
def barcheck(column: str):
    """
    Checks if filter has applied and updates chart everytime button is pressed
        It then calls BarChart() with the selected column
    """
    if filterapply:
        data = tickets.GetAllTickets(filterquery, column)
        print(data)
        barchart(data, column)
    else:
        data = tickets.GetAllTickets("", column)
        print(data)
        barchart(data, column)

def table():
    """
    Display IT tickets in a table format.
    """
    st.divider()
    st.subheader("IT Tickets Table")
    data = tickets.GetAllTickets("", "")
    st.dataframe(data)

def linechart():
    """
    Create and display a line chart of tickets over time.
    """
    st.divider()
    data = tickets.GetDates(filterquery)
    st.line_chart(data, x = "created_date")

def promptticketinfo()->tuple:
    """
    Prompt the user for ticket information and return as a tuple.
    """
    st.subheader("Create New IT Ticket")
    
    ticket_id = st.text_input("Ticket ID")
    priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
    status = st.selectbox("Status", ["open", "in progress", "resolved"])
    category = st.text_input("Category")
    subject = st.text_input("Subject")
    description = st.text_area("Description")
    created_date = st.date_input("Created Date")
    resolved_date = st.date_input("Resolved Date")
    assigned_to = st.text_input("Assigned To")
    
    return (ticket_id, priority, status, category, subject, description, str(created_date), str(resolved_date), assigned_to)

def CUDTicket(action: str, ticket_info: tuple):
    """
    Create, Update, or Delete an IT ticket based on the action specified.
    """
    if action == "Create":
        ticket_id = tickets.insert_ticket(*ticket_info)
        st.success(f"Ticket '{ticket_id}' created successfully.")
    elif action == "Update":
        success = tickets.update_ticket(*ticket_info)
        if success:
            st.success(f"Ticket '{ticket_info[0]}' updated successfully.")
        else:
            st.error(f"Failed to update ticket '{ticket_info[0]}'.")
    elif action == "Delete":
        success = tickets.delete_ticket(ticket_info[0])
        if success:
            st.success(f"Ticket '{ticket_info[0]}' deleted successfully.")
        else:
            st.error(f"Failed to delete ticket '{ticket_info[0]}'.")

def streaming(completion):
    """
    Explanation: Takes delta time and displays ChatGPT response in small chunks
    Args: 
        completion (_Stream[ChatCompletionChunk]_): Contains entire response in small chunks
    Returns:
        fullReply (_str_): Contains the full response by ChatGPT
    """
    container = st.empty()
    fullReply = ""
    
    for chunk in completion:
        delta = chunk.choices[0].delta
        
        # Check if content exists to avoid errors on empty chunks (like stop sequences)
        if delta.content is not None:
            fullReply += delta.content
            container.markdown(fullReply + " ▌") 
    
    # Remove cursor and show final response
    container.markdown(fullReply)
    return fullReply

def AIAssistant():
    """
        Implementing ChatGPT 4o mini to assist with IT related doubts
    """   
    st.divider()
    st.subheader("IT Expert")
    debug(st.session_state.messages)
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    prompt = st.chat_input("Prompt our IT expert (GPT 4.0mini)...")
    gptMsg = [{"role": "system", "content": "You are an IT expert, you hold knowledge specialising in office related IT incidents. Make sure your responses are not too long"}]
    if prompt:
        st.session_state.messages.append({ "role": "user", "content": prompt })
        with st.chat_message("user"): 
            st.markdown(prompt) #Display user prompt in markdown
        
        # Call OpenAI API with streaming
        with st.spinner("Thinking..."):
            completion = client.chat.completions.create( 
                model = "gpt-4o-mini",
                messages = gptMsg + st.session_state.messages,
                stream = True,
            )
            
        # Display streaming response
        with st.chat_message("assistant"):
            fullReply = streaming(completion)
        
        #Save AI response
        st.session_state.messages.append({ "role": "assistant", "content": fullReply })
        debug(st.session_state.messages)

def LogOut():
    """
    Log out the current user and redirect to the login page.
    """
    st.divider()
    if st.button("Log Out", type="primary"):
    # 1. Clear session state
        st.session_state.logged_in = False
        st.session_state.username = "" 
    
    # 2. Redirect immediately
        st.switch_page("Home.py")

if __name__ == "__main__":
    #Global Variables
    filterApply = False 
    filterQuery = ""
    widgetKey: str = ""
    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])
    promptGiven: bool = False
    
    #Preliminary Checks for login
    check_login()
    st.title("IT TICKETS")
    
    #Widgets and UI
    Filters() 
    table()
    sub: str = selectcol()
    RowColumnCnt(sub)
    barcheck(sub)
    linechart()
    CUDTicket()
    AIAssistant()
    LogOut()