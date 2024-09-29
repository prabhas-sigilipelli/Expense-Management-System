import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def analytics_category_tab():
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("start_date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("end_date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        try:
            response = requests.post(f"{API_URL}/analytics/", json=payload)
            #st.write(response.status_code)  # Debugging status code
            #st.write(response.text)         # Debugging raw response text
            response = response.json()      # Convert to JSON
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
            return
        except ValueError:
            st.error("Invalid JSON response from API")
            return

        if response and isinstance(response, dict):
            # Extracting data from dictionary
            data = {
                "Category": list(response.keys()),
                "Total": [response[category]["total"] for category in response],
            }

            # Calculate percentages (optional if not provided by the API)
            total_sum = sum(data["Total"])
            data["Percentage"] = [(total / total_sum) * 100 for total in data["Total"]]

            # Create DataFrame
            df = pd.DataFrame(data)
            df_sorted = df.sort_values(by="Percentage", ascending=False)

            # Chart and table rendering
            st.title("Expense Breakdown By Category")
            st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], use_container_width=True)

            # Formatting Total and Percentage
            df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
            df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
            st.table(df_sorted)
        else:
            st.error("Failed to fetch data or invalid response from API")


