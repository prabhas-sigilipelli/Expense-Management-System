import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def analytics_months_tab():
    # Fetch data from the API
    try:
        response = requests.get(f"{API_URL}/monthly_summary/")
        response.raise_for_status()  # Raise an error for bad response
        monthly_summary = response.json()  # Parse the API response
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from API: {e}")
        return

    # Show raw API response for debugging
    #st.write("API Response:", monthly_summary)

    # Create a DataFrame from the response data
    df = pd.DataFrame(monthly_summary)

    # Debug: Show the DataFrame columns for confirmation
    #st.write("DataFrame columns:", df.columns)

    # Sorting the DataFrame by 'Month_Name' in ascending order (since you don't have month numbers)
    df_sorted = df.sort_values(by="Month_Name", ascending=True)

    # Display the sorted DataFrame as a bar chart
    st.title("Expense Breakdown By Months")
    st.bar_chart(data=df_sorted.set_index("Month_Name")['Total'], use_container_width=True)

    # Format 'Total' column to 2 decimal places for better readability
    df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)

    # Display the sorted DataFrame in a table format
    st.table(df_sorted)


