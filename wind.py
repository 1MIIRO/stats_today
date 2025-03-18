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

# Function to process the data and calculate the highest wind_speed_max per year and month
def calculate_highest_wind_speed_per_year_and_month(data):
    wind_speed_per_year_month = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        wind_speed_max = entry.get('weather', {}).get('wind_speed_max', 0)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            wind_speed_per_year_month[year][month].append(wind_speed_max)
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the highest wind_speed_max for each month of each year
    highest_wind_speed = defaultdict(lambda: defaultdict(dict))
    for year, months in wind_speed_per_year_month.items():
        for month, wind_speeds in months.items():
            highest_wind_speed[year][month]['max_wind_speed'] = max(wind_speeds)
            highest_wind_speed[year][month]['actual_wind_speed'] = wind_speeds[0]  # Use the first entry as actual wind speed

    return highest_wind_speed

# Function to create the 'wind_speed_graphs' folder (delete if exists)
def create_wind_speed_graph_folder():
    folder_path = 'wind_speed_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot the highest wind_speed_max and actual wind_speed_max for all 12 months in one graph for each year
def plot_and_save_wind_speed(highest_wind_speed, folder_path):
    for year, months in highest_wind_speed.items():
        # Prepare the data for the plot
        months_list = []
        max_wind_speed_list = []
        actual_wind_speed_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and wind speed data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            max_wind_speed_list.append(months.get(month, {}).get('max_wind_speed', 0))
            actual_wind_speed_list.append(months.get(month, {}).get('actual_wind_speed', 0))

        # Create a new figure for the year
        plt.figure(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for max wind speed and actual wind speed
        plt.bar(index, max_wind_speed_list, bar_width, label='Max Wind Speed', color='red')
        plt.bar([i + bar_width for i in index], actual_wind_speed_list, bar_width, label='Actual Wind Speed', color='blue')

        plt.xlabel('Month')
        plt.ylabel('Wind Speed (km/h or mph)')
        plt.title(f'Highest and Actual Wind Speed in {year}')
        plt.xticks([i + bar_width / 2 for i in index], months_list)  # Center the ticks between the bars
        plt.legend()

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/wind_speed_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_graphs\\merged_data.json')

    # Calculate highest and actual wind_speed_max per year and month
    highest_wind_speed = calculate_highest_wind_speed_per_year_and_month(data)

    # Create the 'wind_speed_graphs' folder
    folder_path = create_wind_speed_graph_folder()

    # Generate and save wind speed graphs for each year
    plot_and_save_wind_speed(highest_wind_speed, folder_path)

    print(f"Wind speed graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
