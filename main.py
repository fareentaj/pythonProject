import pandas as pd
import matplotlib.pyplot as plt

# Assuming the data is in a CSV file called 'flight_data.csv' with columns:
# 'route', 'departure_time', 'departure_airport', 'arrival_airport', 'passengers'

# Read the data into a pandas DataFrame
flight_data = pd.read_csv(r'flight_data.csv')
flight_data['departure_time'] = pd.to_datetime(flight_data['departure_time'])


# Function to filter flights based on the time of the day (AM/PM) and the selected routes
def filter_flights(route1, route2, am_pm):
    am = (flight_data['departure_time'].dt.hour >= 0) & (flight_data['departure_time'].dt.hour < 12)
    pm = (flight_data['departure_time'].dt.hour >= 12) & (flight_data['departure_time'].dt.hour < 24)

    if am_pm == 'AM':
        time_filter = am
    else:
        time_filter = pm

    filtered_flights = flight_data[(flight_data['route'].isin([route1, route2])) & time_filter]
    return filtered_flights


# Function to plot passenger trends for AM and PM flights
def plot_am_pm_trends(route1, route2):
    am_flights = filter_flights(route1, route2, 'AM').groupby('route')['passengers'].sum()
    pm_flights = filter_flights(route1, route2, 'PM').groupby('route')['passengers'].sum()

    fig, ax = plt.subplots()
    ax.bar(am_flights.index, am_flights, label='AM Flights', alpha=0.6)
    ax.bar(pm_flights.index, pm_flights, label='PM Flights', alpha=0.6)
    ax.set_ylabel('Passengers')
    ax.set_title('Passenger Trends for AM and PM Flights')
    ax.legend()
    plt.show()


# Function to find and plot the departure airport with the most passengers
def plot_busiest_departure_airport():
    busiest_airport = flight_data.groupby('departure_airport')['passengers'].sum().idxmax()
    busiest_airport_data = flight_data[flight_data['departure_airport'] == busiest_airport]

    monthly_data = busiest_airport_data.groupby(busiest_airport_data['departure_time'].dt.to_period('M'))[
        'passengers'].sum()
    monthly_data.plot(kind='line', marker='o', title='Passenger Trend for Busiest Departure Airport')
    plt.ylabel('Passengers')
    plt.show()


# Example usage
route1 = 'route_A'
route2 = 'route_B'
plot_am_pm_trends(route1, route2)
plot_busiest_departure_airport()
