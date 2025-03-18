import json
import os
import matplotlib.pyplot as plt
import calendar
from collections import defaultdict
from datetime import datetime
import shutil

# Function to load data from a JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to create the folder if it doesn't exist (or delete and recreate it if it does)
def create_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)  # Delete the existing folder and its contents
    os.makedirs(folder_name)  # Create a new folder

# Load data and create folder
data = load_json_data('bar_line\\merged_data.json')  # Replace with your actual file path
create_folder('graphs_rainfall_snowfall')  # Folder to store this specific plot

# Process data to get rainfall and snowfall
def calculate_rainfall_snowfall(data):
    monthly_data = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        rain_sum = entry.get('weather', {}).get('rain_sum', 0)
        snowfall_sum = entry.get('weather', {}).get('snowfall_sum', 0)

        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            monthly_data[year][month].append({
                'rain_sum': rain_sum,
                'snowfall_sum': snowfall_sum,
            })
        except ValueError:
            continue  # Skip invalid date entries

    year_month_totals = defaultdict(lambda: defaultdict(dict))
    for year, months in monthly_data.items():
        for month, values in months.items():
            total_rainfall = sum(entry['rain_sum'] for entry in values)
            total_snowfall = sum(entry['snowfall_sum'] for entry in values)
            year_month_totals[year][month] = {
                'total_rainfall': total_rainfall,
                'total_snowfall': total_snowfall,
            }

    return year_month_totals

# Plot the graph
def plot_rainfall_snowfall(year_month_totals):
    for year, months in year_month_totals.items():
        months_list = [calendar.month_abbr[i] for i in range(1, 13)]
        total_rainfall_list = [months.get(i, {}).get('total_rainfall', 0) for i in range(1, 13)]
        total_snowfall_list = [months.get(i, {}).get('total_snowfall', 0) for i in range(1, 13)]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax2 = ax1.twinx()
        # Plot line for rainfall first to make sure it's on top
        ax2.plot(months_list, total_rainfall_list, label='Rainfall (mm)', color='blue', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Rainfall (mm)', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        # Plot the bars for snowfall
        ax1.bar(months_list, total_snowfall_list, label='Snowfall (cm)', color='cyan', alpha=0.6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Snowfall (cm)', color='cyan')
        ax1.tick_params(axis='y', labelcolor='cyan')

        plt.title(f'Rainfall & Snowfall in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.savefig(f'graphs_rainfall_snowfall/rainfall_snowfall_{year}.png')
        plt.close()

# Calculate and plot
year_month_totals = calculate_rainfall_snowfall(data)
plot_rainfall_snowfall(year_month_totals)
