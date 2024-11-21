
# Customized Bus Route Search Platform

This is a web-based platform built with **Streamlit** that allows users to search for bus routes across various states in India, based on customizable filters such as route name, price range, departure time, bus type, and star ratings.

## Features

- **State-wise Route Search**: Users can select a state and see available bus routes.
- **Filter Options**:
  - **Price Range**: Filter buses based on their price range (e.g., 0-500, 500-1000, etc.).
  - **Departure Time**: Filter buses based on the time of departure (e.g., 12:00 AM to 01:00 AM).
  - **Star Rating**: Filter based on bus ratings, with options ranging from 0 to 5 stars.
  - **Bus Type**: Filter based on bus types such as AC, Non-AC, Sleeper, Seater.

- **Data from MySQL**: The data is fetched dynamically from a MySQL database.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python, MySQL
- **Database**: MySQL
- **Libraries**:
  - Pandas
  - PyMySQL
  - Datetime
  - Streamlit

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/customized-bus-route-search.git
   ```

2. Navigate to the project directory:
   ```bash
   cd customized-bus-route-search
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## How to Use

1. **Select State**: Use the state dropdown in the sidebar to select the state for which you want to search bus routes.
2. **Select Route**: After selecting a state, choose a specific route or select "All Routes" to view all available routes.
3. **Price Range**: Filter buses by selecting a price range.
4. **Departure Time**: Select a departure time range to filter buses based on when they depart.
5. **Star Rating**: Filter buses by their star rating, U can also select multiple option.
6. **Bus Type**: Choose from different bus types like AC, Non-AC, Sleeper, and Seater.


## Database Schema

The MySQL database contains a table named **bus_details** with the following columns:

| Column            | Description                                   |
|-------------------|-----------------------------------------------|
| ID                | Unique identifier for each bus route          |
| State Name        | The state in which the bus operates           |
| Route Name        | The name of the bus route                     |
| Route Link        | Link to the route details                     |
| Bus Name          | Name of the bus                               |
| Bus Type          | Type of bus (e.g., AC, Non-AC, Sleeper)       |
| Departing Time    | Departure time of the bus                     |
| Duration          | Duration of the journey                       |
| Reaching Time     | Time the bus reaches the destination          |
| Star Rating       | Rating of the bus based on user feedback      |
| Price             | Price of the bus ticket                       |
| Seats Available   | Number of available seats in the bus          |

## Contribution

If you want to contribute to this project, feel free to fork the repository and create a pull request. Here's how you can contribute:

1. Fork this repository.
2. Create a new branch for your feature.
3. Make the necessary changes or additions.
4. Submit a pull request with a description of your changes.



## Acknowledgements

- **Streamlit** for building the interactive web application.
- **MySQL** for managing the database.
- **Pandas** and **PyMySQL** for data handling and SQL connectivity.
