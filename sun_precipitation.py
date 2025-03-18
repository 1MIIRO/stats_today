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

# Function to convert sunshine seconds to hours
def get_sunshine_duration(sunshine_seconds):
    sunshine_seconds = float(sunshine_seconds)
    return sunshine_seconds / 3600  # Convert seconds to hours

# Function to process the data and calculate sunshine hours and precipitation hours for each year and month
def calculate_sunshine_and_precipitation_per_year_and_month(data):
    sunshine_precipitation_per_year_month = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        sunshine_seconds = entry.get('weather', {}).get('sunshine_hours', 0)
        precipitation_hours = entry.get('weather', {}).get('precipitation_hours', 0)

        # Convert sunshine seconds to sunshine hours
        sunshine_hours = get_sunshine_duration(sunshine_seconds)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            sunshine_precipitation_per_year_month[year][month].append((sunshine_hours, precipitation_hours))
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the sunshine hours and precipitation hours for each month of each year
    sunshine_precipitation_data = defaultdict(lambda: defaultdict(dict))
    for year, months in sunshine_precipitation_per_year_month.items():
        for month, values in months.items():
            # Calculate the average sunshine hours for the month
            avg_sunshine_hours = sum(sunshine_hours for sunshine_hours, _ in values) / len(values)
            # Calculate the total precipitation hours for the month
            total_precipitation_hours = sum(precipitation_hours for _, precipitation_hours in values)

            sunshine_precipitation_data[year][month]['avg_sunshine_hours'] = avg_sunshine_hours
            sunshine_precipitation_data[year][month]['total_precipitation_hours'] = total_precipitation_hours

    return sunshine_precipitation_data

# Function to create the 'sunshine_precipitation_graphs' folder (delete if exists)
def create_sunshine_precipitation_graph_folder():
    folder_path = 'sunshine_precipitation_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot and save the sunshine hours and precipitation hours for each month in a year
def plot_and_save_sunshine_precipitation(sunshine_precipitation_data, folder_path):
    for year, months in sunshine_precipitation_data.items():
        # Prepare the data for the plot
        months_list = []
        avg_sunshine_hours_list = []
        total_precipitation_hours_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and sunshine and precipitation data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            avg_sunshine_hours_list.append(months.get(month, {}).get('avg_sunshine_hours', 0))
            total_precipitation_hours_list.append(months.get(month, {}).get('total_precipitation_hours', 0))

        # Create a new figure for the year
        fig, ax1 = plt.subplots(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for precipitation hours
        ax1.bar(index, total_precipitation_hours_list, bar_width, label='Total Precipitation Hours', color='blue', alpha=0.6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Total Precipitation Hours', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticks([i for i in index])
        ax1.set_xticklabels(months_list)

        # Create a secondary y-axis to plot sunshine hours
        ax2 = ax1.twinx()
        ax2.plot(index, avg_sunshine_hours_list, label='Average Sunshine Hours', color='red', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Average Sunshine Hours', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Title and legend
        plt.title(f'Sunshine Hours and Precipitation in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/sunshine_precipitation_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_line\\merged_data.json')

    # Calculate the sunshine hours and precipitation hours per year and month
    sunshine_precipitation_data = calculate_sunshine_and_precipitation_per_year_and_month(data)

    # Create the 'sunshine_precipitation_graphs' folder
    folder_path = create_sunshine_precipitation_graph_folder()

    # Generate and save sunshine and precipitation graphs for each year
    plot_and_save_sunshine_precipitation(sunshine_precipitation_data, folder_path)

    print(f"Sunshine and precipitation graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
