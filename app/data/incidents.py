import pandas as pd
from app.data.db import connect_database

def insert_incident(id, date, incident_type, severity, status):
    """
    Adds a new incident record to the database and returns the new ID.
    """
    # 1. Connect to the DB
    db = connect_database()
    cursor = db.cursor()

    # 2. Run the SQL Command
    sql = """
        INSERT INTO cyber_incidents 
        (id, date, incident_type, severity, status)
        VALUES (?, ?, ?, ?, ?)
    """
    values = (id, date, incident_type, severity, status)
    
    cursor.execute(sql, values)
    db.commit()
    db.close()


def update_incident(id, date, incident_type, severity, status):
    """
    Updates an existing incident record in the database.
    Returns True if successful, False otherwise.
    """
    # 1. Connect to the DB
    db = connect_database()
    cursor = db.cursor()

    # 2. Run the SQL Command
    sql = """
        UPDATE cyber_incidents
        SET date = ?, incident_type = ?, severity = ?, status = ?
        WHERE id = ?
    """
    values = (date, incident_type, severity, status, id)
    
    cursor.execute(sql, values)
    db.commit()

    # 3. Check if any row was updated
    success = cursor.rowcount > 0
    
    db.close()
    return success

def delete_incident(incident_id):
    """
    Deletes an incident record from the database by its ID.
    Returns True if successful, False otherwise.
    """
    # 1. Connect to the DB
    db = connect_database()
    cursor = db.cursor()

    # 2. Run the SQL Command
    sql = "DELETE FROM cyber_incidents WHERE id = ?"
    cursor.execute(sql, (incident_id,))
    db.commit()

    # 3. Check if any row was deleted
    success = cursor.rowcount > 0
    
    db.close()
    return success

def get_groupby(column):
    """
    Retrieves distinct values for a specified column from the cyber_incidents table.
    """
    # 1. Establish connection
    db = connect_database()
    
    # 2. Generate the full SQL command
    sql_command = f"SELECT {column},COUNT(*) FROM cyber_incidents GROUP BY {column}"
    
    # 3. Execute query and load directly into a Pandas DataFrame
    results_df = pd.read_sql_query(sql_command, db)
    print(results_df)
    
    # 4. Close connection and return data
    db.close()
    return results_df


def get_all_incidents(filter_str,column):
    """
    Retrieves distinct values for a specified column from the cyber_incidents table.
    """
    # 1. Establish connection
    db = connect_database()
    
    # 2. Generate the full SQL command
    sql_command = f"SELECT {column},COUNT(*) FROM cyber_incidents GROUP BY {column}"
    
    # 3. Execute query and load directly into a Pandas DataFrame
    results_df = pd.read_sql_query(sql_command, db)
    print(results_df)
    
    # 4. Close connection and return data
    db.close()
    return results_df

def get_dataframequery(filter_str):
    """
    Returns the DataFrame
    """
    # 1. Establish connection
    db = connect_database()
    
    # 2. Generate the full SQL command using the helper function
    sql_command = 'Select * from cyber_incidents'
    
    # 3. Execute query and load directly into a Pandas DataFrame
    results_df = pd.read_sql_query(sql_command, db)
    print(results_df)
    
    # 4. Close connection and return data
    db.close()
    return results_df
   


def get_incidents_query(filter_str,column):
    """
    Builds the SQL query to select incident types.
    Appends a WHERE clause only if a filter string is provided.
    """
    # 1. Define the base requirement
    query = "SELECT "+column+" FROM cyber_incidents"
    
    # 2. Add the condition if it exists
    if filter_str:
        query += f" WHERE {filter_str}"
    print('Filter string 1',filter_str)
    
    return query

def droptable():
    """
    Drops the cyber_incidents table from the database.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE cyber_incidents")
    conn.commit()
    conn.close()

def total_incidents(filter_str: str) -> int:
    """
    Executes the query with the optional filter and returns the total count of matches.
    """
    # 1. Open Connection
    conn = connect_database()
    
    # 2. Get the SQL string
    sql_cmd = get_incidents_query(filter_str)
    
    # 3. Load results into a DataFrame
    df_results = pd.read_sql_query(sql_cmd, conn)
    
    conn.close()
    
    # 4. Return the number of rows found
    return len(df_results)

def transfer_csv():
    import csv
    from pathlib import Path
    
    conn = connect_database()
    cursor = conn.cursor()
    
    with open(Path("DATA/cyber_incidents.csv")) as csv_file:
        reader = csv.reader(csv_file)
                   
        next(reader)
        
        for row in reader:
            cursor.execute("""
                INSERT INTO cyber_incidents 
                (id,date, incident_type, severity, status)
                VALUES ( ?, ?, ?, ?, ?)
            """, (row[0],row[1], row[2], row[3], row[4]))
            
    conn.commit()
    conn.close()