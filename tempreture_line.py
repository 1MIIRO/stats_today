import json
import matplotlib.pyplot as plt
import os
import shutil
from collections import defaultdict
from datetime import datetime
import calendar

# Function to load data from a JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to process the data and calculate average temperatures per year and month
def calculate_avg_temperatures_per_year_and_month(data):
    temp_per_year_month = defaultdict(lambda: defaultdict(lambda: {'temperature_max': [], 'temperature_min': [], 'temperature_mean': []}))

    for entry in data:
        date = entry.get('date', '')
        temperature_max = entry.get('weather', {}).get('temperature_max', 0)
        temperature_min = entry.get('weather', {}).get('temperature_min', 0)
        temperature_mean = entry.get('weather', {}).get('temperature_mean', 0)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            temp_per_year_month[year][month]['temperature_max'].append(temperature_max)
            temp_per_year_month[year][month]['temperature_min'].append(temperature_min)
            temp_per_year_month[year][month]['temperature_mean'].append(temperature_mean)
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate average temperatures for each month of each year
    avg_temperatures = defaultdict(lambda: defaultdict(dict))
    for year, months in temp_per_year_month.items():
        for month, temps in months.items():
            avg_temperatures[year][month]['temperature_max'] = sum(temps['temperature_max']) / len(temps['temperature_max']) if temps['temperature_max'] else 0
            avg_temperatures[year][month]['temperature_min'] = sum(temps['temperature_min']) / len(temps['temperature_min']) if temps['temperature_min'] else 0
            avg_temperatures[year][month]['temperature_mean'] = sum(temps['temperature_mean']) / len(temps['temperature_mean']) if temps['temperature_mean'] else 0

    return avg_temperatures

# Function to create the 'temperature_graphs' folder (delete if exists)
def create_temperature_graph_folder():
    folder_path = 'temperature_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot the temperature averages for all 12 months in one graph for each year
def plot_and_save_temperature_averages(avg_temperatures, folder_path):
    for year, months in avg_temperatures.items():
        # Prepare the data for the plot
        months_list = []
        max_temp_list = []
        min_temp_list = []
        mean_temp_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and temperature data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            max_temp_list.append(months.get(month, {}).get('temperature_max', 0))
            min_temp_list.append(months.get(month, {}).get('temperature_min', 0))
            mean_temp_list.append(months.get(month, {}).get('temperature_mean', 0))

        # Create a new figure for the year
        plt.figure(figsize=(10, 6))
        plt.plot(months_list, max_temp_list, label='Max Temperature', marker='o', color='red')
        plt.plot(months_list, min_temp_list, label='Min Temperature', marker='o', color='blue')
        plt.plot(months_list, mean_temp_list, label='Mean Temperature', marker='o', color='green')

        plt.xlabel('Month')
        plt.ylabel('Temperature (°C)')
        plt.title(f'Average Temperatures in {year}')
        plt.legend()

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/temperature_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_graphs\\merged_data.json')

    # Calculate average temperatures per year and month
    avg_temperatures = calculate_avg_temperatures_per_year_and_month(data)

    # Create the 'temperature_graphs' folder
    folder_path = create_temperature_graph_folder()

    # Generate and save temperature graphs for each year
    plot_and_save_temperature_averages(avg_temperatures, folder_path)

    print(f"Temperature graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
