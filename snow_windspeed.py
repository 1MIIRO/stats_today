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

# Function to process the data and calculate the total snowfall_sum, and maximum wind_speed per year and month
def calculate_wind_speed_snowfall_per_year_and_month(data):
    wind_speed_snowfall_per_year_month = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        wind_speed_max = entry.get('weather', {}).get('wind_speed_max', 0)
        snowfall_sum = entry.get('weather', {}).get('snowfall_sum', 0)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            wind_speed_snowfall_per_year_month[year][month].append((wind_speed_max, snowfall_sum))
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the total snowfall_sum, and maximum wind_speed for each month of each year
    total_wind_speed_snowfall = defaultdict(lambda: defaultdict(dict))
    for year, months in wind_speed_snowfall_per_year_month.items():
        for month, values in months.items():
            total_snowfall_sum = sum(snowfall_sum for _, snowfall_sum in values)  # Total snowfall sum
            max_wind_speed = max(wind_speed_max for wind_speed_max, _ in values)  # Maximum wind speed
            
            total_wind_speed_snowfall[year][month]['total_snowfall_sum'] = total_snowfall_sum
            total_wind_speed_snowfall[year][month]['max_wind_speed'] = max_wind_speed

    return total_wind_speed_snowfall

# Function to create the 'wind_speed_snowfall_graphs' folder (delete if exists)
def create_wind_speed_snowfall_graph_folder():
    folder_path = 'wind_speed_snowfall_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot and save the maximum wind speed and total snowfall_sum for each month in a year
def plot_and_save_wind_speed_snowfall(total_wind_speed_snowfall, folder_path):
    for year, months in total_wind_speed_snowfall.items():
        # Prepare the data for the plot
        months_list = []
        max_wind_speed_list = []
        total_snowfall_sum_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and wind speed and snowfall data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            max_wind_speed_list.append(months.get(month, {}).get('max_wind_speed', 0))
            total_snowfall_sum_list.append(months.get(month, {}).get('total_snowfall_sum', 0))

        # Create a new figure for the year
        fig, ax1 = plt.subplots(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for total snowfall (total_snowfall_sum)
        ax1.bar(index, total_snowfall_sum_list, bar_width, label='Total Snowfall (cm)', color='blue', alpha=0.6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Total Snowfall (cm)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticks([i for i in index])
        ax1.set_xticklabels(months_list)

        # Create a secondary y-axis to plot the max wind speed
        ax2 = ax1.twinx()
        ax2.plot(index, max_wind_speed_list, label='Max Wind Speed (km/h)', color='red', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Max Wind Speed (km/h)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Title and legend
        plt.title(f'Max Wind Speed and Total Snowfall in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/wind_speed_snowfall_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_line\\merged_data.json')

    # Calculate total snowfall_sum, and maximum wind_speed per year and month
    total_wind_speed_snowfall = calculate_wind_speed_snowfall_per_year_and_month(data)

    # Create the 'wind_speed_snowfall_graphs' folder
    folder_path = create_wind_speed_snowfall_graph_folder()

    # Generate and save wind speed and snowfall graphs for each year
    plot_and_save_wind_speed_snowfall(total_wind_speed_snowfall, folder_path)

    print(f"Wind speed and snowfall graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
