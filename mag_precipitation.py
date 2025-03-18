import json
import os
import matplotlib.pyplot as plt
import calendar
from collections import defaultdict
from datetime import datetime
import shutil

# Load data from JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Create folder if not exists, or delete and recreate if it exists
def create_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)  # Delete the existing folder and its contents
    os.makedirs(folder_name)  # Create a new folder

# Load data and create folder
data = load_json_data('bar_line\\merged_data.json')  # Replace with your actual file path
create_folder('graphs_magnitude_precipitation')  # Folder to store this specific plot

# Process data to get magnitude and precipitation hours
def calculate_magnitude_precipitation(data):
    monthly_data = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        magnitude = entry.get('magnitude', 0)
        precipitation_hours = entry.get('weather', {}).get('precipitation_hours', 0)

        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            monthly_data[year][month].append({
                'magnitude': magnitude,
                'precipitation_hours': precipitation_hours,
            })
        except ValueError:
            continue  # Skip invalid date entries

    year_month_averages = defaultdict(lambda: defaultdict(dict))
    for year, months in monthly_data.items():
        for month, values in months.items():
            avg_magnitude = sum(entry['magnitude'] for entry in values) / len(values)
            avg_precipitation_hours = sum(entry['precipitation_hours'] for entry in values) / len(values)
            year_month_averages[year][month] = {
                'avg_magnitude': avg_magnitude,
                'avg_precipitation_hours': avg_precipitation_hours,
            }

    return year_month_averages

# Plot the graph
def plot_magnitude_precipitation(year_month_averages):
    for year, months in year_month_averages.items():
        months_list = [calendar.month_abbr[i] for i in range(1, 13)]
        avg_magnitude_list = [months.get(i, {}).get('avg_magnitude', 0) for i in range(1, 13)]
        avg_precipitation_hours_list = [months.get(i, {}).get('avg_precipitation_hours', 0) for i in range(1, 13)]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax2 = ax1.twinx()
        ax2.plot(months_list, avg_magnitude_list, label='Magnitude', color='green', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Magnitude', color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        ax1.bar(months_list, avg_precipitation_hours_list, label='Precipitation Hours', color='purple', alpha=0.6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Precipitation Hours', color='purple')
        ax1.tick_params(axis='y', labelcolor='purple')

        plt.title(f'Magnitude & Precipitation Hours in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.savefig(f'graphs_magnitude_precipitation/magnitude_precipitation_{year}.png')
        plt.close()

# Calculate and plot
year_month_averages = calculate_magnitude_precipitation(data)
plot_magnitude_precipitation(year_month_averages)
