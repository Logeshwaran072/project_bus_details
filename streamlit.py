from datetime import datetime
import streamlit as st
import pandas as pd
import pymysql

# Title
st.set_page_config(page_title="State-wise Bus Route Details", layout="wide")

st.title("Customized Bus Route Search Platform")

# SQL connection
connection = pymysql.connect(
    host="127.0.0.1", user="root", passwd="Logesh007$", database="redbus"
)

def fetch_all_data():
    """
    Fetch all data from the database.
    This function queries the entire bus_details table.
    """
    try:
        query = "SELECT * FROM bus_details"
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []


def apply_filters(data, filters):
    """
    Apply multiple filters to the data.
    Filters should be a dictionary with keys matching filter criteria.
    """
    if all(value in [None, "", [], "All State", "All Routes"] for value in filters.values()):
        return data

    # Apply filters sequentially
    for key, value in filters.items():
        if key == "state_name" and value != "All State" and value:
            data = [row for row in data if row[1] == value]
        elif key == "route_name" and value != "All Routes" and value:
            data = [row for row in data if row[2] == value]
        elif key == "price_range" and value != "other" and value:
            if value == "0-500":
                data = [row for row in data if 0 <= row[10] <= 500]
            elif value == "500-1000":
                data = [row for row in data if 500 < row[10] <= 1000]
            elif value == "1000-2000":
                data = [row for row in data if 1000 < row[10] <= 2000]
            elif value == "2000 and above":
                data = [row for row in data if row[10] > 2000]
        elif key == "departing_time" and value:
            time_ranges = [
                (datetime.strptime(start, "%I:%M %p").time(), datetime.strptime(end, "%I:%M %p").time())
                for start, end in value
            ]
            data = [row for row in data if any(start <= datetime.strptime(row[6], "%H:%M").time() <= end for start, end in time_ranges)]
        elif key == "star_rating" and value:
            data = [
                row for row in data if any(lower <= row[9] <= upper for lower, upper in value)
            ]
        elif key == "bus_type" and value:
            # Updated filtering logic
            bus_types = {
                "AC": r"\bAC\b",
                "Non AC": r"\bNon AC\b",
                "Sleeper": r"\bSleeper\b",
                "Seater": r"\bSeater\b",
            }
            for v in value:
                regex = bus_types.get(v, "")
                data = [row for row in data if pd.Series(row[5]).str.contains(regex, case=False).any()]

    return data

# Fetch all data from the database
all_data = fetch_all_data()

if all_data:
    # Convert fetched data to a Pandas DataFrame
    columns = [
        "ID",
        "State Name",
        "Route Name",
        "Route Link",
        "Bus Name",
        "Bus Type",  # AC/Non-AC, Sleeper/Seater information stored here
        "Departing Time",
        "Duration",
        "Reaching Time",
        "Star Rating",
        "Price",
        "Seats Available",
    ]
    df = pd.DataFrame(all_data, columns=columns)

    # Sidebar filters
    state_name = st.sidebar.selectbox("Select a state", ["All State"] + list(df["State Name"].unique()))

    if state_name !='All State':
        state_name_filter = [row for row in all_data if row[1] == state_name]
        routes = sorted(set([row[2] for row in state_name_filter]))
        
    else :
        routes = list(set([row[2] for row in all_data]))
    route_name = st.sidebar.selectbox("Select a route", ["All Routes"] + routes)

    price_range = st.sidebar.radio(
        "Select the price range",
        ("0-500", "500-1000", "1000-2000", "2000 and above","other"),
        index=4,
    )
    time_ranges_display = {
        "12:00am - 01:00am": ("12:00 AM", "01:00 AM"),
        "01:00am - 02:00am": ("01:00 AM", "02:00 AM"),
        "02:00am - 03:00am": ("02:00 AM", "03:00 AM"),
        "03:00am - 04:00am": ("03:00 AM", "04:00 AM"),
        "04:00am - 05:00am": ("04:00 AM", "05:00 AM"),
        "05:00am - 06:00am": ("05:00 AM", "06:00 AM"),
        "06:00am - 07:00am": ("06:00 AM", "07:00 AM"),
        "07:00am - 08:00am": ("07:00 AM", "08:00 AM"),
        "08:00am - 09:00am": ("08:00 AM", "09:00 AM"),
        "09:00am - 10:00am": ("09:00 AM", "10:00 AM"),
        "10:00am - 11:00am": ("10:00 AM", "11:00 AM"),
        "11:00am - 12:00pm": ("11:00 AM", "12:00 PM"),
        "12:00pm - 01:00pm": ("12:00 PM", "01:00 PM"),
        "01:00pm - 02:00pm": ("01:00 PM", "02:00 PM"),
        "02:00pm - 03:00pm": ("02:00 PM", "03:00 PM"),
        "03:00pm - 04:00pm": ("03:00 PM", "04:00 PM"),
        "04:00pm - 05:00pm": ("04:00 PM", "05:00 PM"),
        "05:00pm - 06:00pm": ("05:00 PM", "06:00 PM"),
        "06:00pm - 07:00pm": ("06:00 PM", "07:00 PM"),
        "07:00pm - 08:00pm": ("07:00 PM", "08:00 PM"),
        "08:00pm - 09:00pm": ("08:00 PM", "09:00 PM"),
        "09:00pm - 10:00pm": ("09:00 PM", "10:00 PM"),
        "10:00pm - 11:00pm": ("10:00 PM", "11:00 PM"),
        "11:00pm - 12:00am": ("11:00 PM", "12:00 AM"),
    }
    selected_time_range_label = st.sidebar.select_slider(
        "Select departure Time",
        [""] + list(time_ranges_display.keys())
    )
    selected_time_range = (
        time_ranges_display[selected_time_range_label]
        if selected_time_range_label != ""
        else None
    )
    star_rating_ranges = st.sidebar.multiselect(
        "Select depature rating",
        [
            "0 to 1",
            "1 to 2",
            "2 to 3",
            "3 to 4",
            "4 to 5",
        ],
        default=[],
    )
    star_rating_mapping = {
        "0 to 1": (0, 1),
        "1 to 2": (1, 2),
        "2 to 3": (2, 3),
        "3 to 4": (3, 4),
        "4 to 5": (4, 5),
    }
    star_rating_ranges = [star_rating_mapping[r] for r in star_rating_ranges]

    # Bus Type Filter
    bus_type_filter = st.sidebar.multiselect(
        "Select Bus Type",
        ["AC", "Non AC", "Sleeper", "Seater"]
    )

    # Define all filters
    filters = {
        "state_name": state_name,
        "route_name": route_name,
        "price_range": price_range,
        "departing_time": [selected_time_range] if selected_time_range else [],
        "star_rating": star_rating_ranges,
        "bus_type": bus_type_filter,
    }

    # Apply filters
    filtered_data = apply_filters(all_data, filters)

    # Display filtered data
    if filtered_data:
        final_df = pd.DataFrame(filtered_data, columns=columns)
        st.write("Filtered Bus Details:")
        st.dataframe(final_df)
    else:
        st.warning("No Buses found for the selected filters.")
   

else:
    st.warning("No data found in the database!")
